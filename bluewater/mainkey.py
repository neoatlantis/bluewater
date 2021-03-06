from .event import Event
from .scrypt import Scrypt

class Mainkey:
    
    FIREBASE_MAINKEY = "__main_key__"

    def __init__(self, session):
        self.session = session
        self.__bindEvents()

    def __bindEvents(self):
        self.eventUninitialized = Event()
        self.eventUndecrypted = Event()
        self.eventDecrypted = Event()
        self.session.eventLogin.append(self.onLogin)
        self.session.eventLogout.append(self.onLogout)

    def __getMainkeyPath(self):
        uid = self.session.getCurrentUser().uid
        return "/" + uid + "/" + self.FIREBASE_MAINKEY

    async def __securePassphrase(self, passphrase):
        key = await Scrypt(passphrase, self.session.getCurrentUser().uid)
        return key

    async def onLogin(self):
        """Fetch main key."""
        getMainkey = await firebase.database().ref(self.__getMainkeyPath())\
            .once("value")
        self.mainkey = getMainkey.val()
        if not self.mainkey:
            console.log("Mainkey not set.")
            self.eventUninitialized.call() 
        else:
            console.log("Mainkey retrieved.")
            self.eventUndecrypted.call()

    async def onLogout(self):
        """Clear all stored keys."""
        self.privateKey = None
        self.publicKey = None

    async def decryptMainkey(self, passphrase):
        # if error, raise eventUndecrypted again
        key = await self.__securePassphrase(passphrase)
        try:
            self.privateKey = openpgp.key.readArmored(self.mainkey)["keys"][0]
            await self.privateKey.decrypt(key)
        except:
            pass
        finally:
            if \
                self.privateKey and\
                self.privateKey.primaryKey and\
                self.privateKey.primaryKey.isDecrypted\
            :
                # decryption confirmed successful
                console.log("Private key decrypted.")
                self.publicKey = self.privateKey.toPublic()
                self.eventDecrypted.call()
                console.log(self.publicKey.armor())
                return True
            else:
                console.error("Private key decryption failure.")
                self.eventUndecrypted.call()
        return False

    async def setMainPassphrase(self, passphrase):
        uid = self.session.getCurrentUser().uid
        key = await self.__securePassphrase(passphrase)
        options = {
            "userIds": [{ "name": uid }],
            "curve": "ed25519",
            "passphrase": key,
        }
        keyPair = await openpgp.generateKey(options)
        privateKey = keyPair.privateKeyArmored
        await firebase.database().ref(self.__getMainkeyPath())\
            .set(privateKey)
        return True
