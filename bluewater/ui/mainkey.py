__pragma__("alias", "S", "$")

##############################################################################

class UIMainkeyInitializer:

    DIALOG_INIT = "#mainkey-init"

    def __init__(self, mainkey):
        self.mainkey = mainkey
        self.__initUI()
        self.__bindEvents()

    def __initUI(self):
        S(self.DIALOG_INIT).dialog({
            "dialogClass": "no-close",
            "autoOpen": False,
            "closeOnEscape": False,
            "modal": True,
            "buttons": {
                "Set Main Passphrase": self.onSetMainPassphrase,
            }
        })

    def __bindEvents(self):
        pass

    def open(self):
        S(self.DIALOG_INIT).dialog("open")

    def close(self):
        S(self.DIALOG_INIT).dialog("close")

    async def onSetMainPassphrase(self):
        # collect parameters and call service!
        password1 = S(self.DIALOG_INIT).find('[name="password1"]').val()
        password2 = S(self.DIALOG_INIT).find('[name="password2"]').val()
        console.log("set", password1, password2)
        await self.mainkey.setMainPassphrase(password1)
        self.close()

##############################################################################

class UIMainkeyDecryptor:

    DIALOG_DECRYPT = "#mainkey-decrypt"

    def __init__(self, mainkey):
        self.mainkey = mainkey
        self.__initUI()
        self.__bindEvents()

    def __initUI(self):
        S(self.DIALOG_DECRYPT).dialog({
            "dialogClass": "no-close",
            "autoOpen": False,
            "closeOnEscape": False,
            "modal": True,
            "buttons": {
                "Decrypt": self.onDecrypt,
            }
        })

    def __bindEvents(self):
        pass

    def onDecrypt(self):
        password = S(self.DIALOG_INIT).find('[name="password"]').val()
        await self.mainkey.decryptMainkey(password)
        self.close()

    def close(self):
        S(self.DIALOG_DECRYPT).dialog("close")

    def open(self):
        S(self.DIALOG_DECRYPT).dialog("open")

##############################################################################

class UIMainkey:

    def __init__(self, mainkey):
        self.mainkey = mainkey
        self.uiMainkeyInitializer = UIMainkeyInitializer(mainkey)
        self.uiMainkeyDecryptor   = UIMainkeyDecryptor(mainkey)
        self.__bindEvents()

    def __bindEvents(self):
        self.mainkey.eventUninitialized.append(self.onUninitialized)
        self.mainkey.eventUndecrypted.append(self.onUndecrypted)

    def onUninitialized(self):
        self.uiMainkeyInitializer.open()

    def onUndecrypted(self):
        self.uiMainkeyDecryptor.open()
