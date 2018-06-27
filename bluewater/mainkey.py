from .event import Event

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

    def __getMainkeyPath(self):
        uid = self.session.getCurrentUser().uid
        return "/" + uid + "/" + self.FIREBASE_MAINKEY

    async def onLogin(self):
        """Fetch main key."""
        getMainkey = await firebase.database().ref(self.__getMainkeyPath())\
            .once("value")
        self.mainkey = getMainkey.val()
        if not self.mainkey:
            console.log("Mainkey not set.")
            self.eventUninitialized.call() 
        else:
            console.log("Mainkey got.", self.mainkey)
            self.eventUndecrypted.call()

    async def decryptMainkey(self, passphrase):
        # if error, raise eventUndecrypted again
        return False

    async def setMainPassphrase(self, passphrase):
        uid = self.session.getCurrentUser().uid
        options = {
            "userIds": [{ "name": uid }],
            "curve": "ed25519",
            "passphrase": passphrase,
        }
        keyPair = await openpgp.generateKey(options)
        privateKey = keyPair.privateKeyArmored
        await firebase.database().ref(self.__getMainkeyPath())\
            .set(privateKey)
        return True
