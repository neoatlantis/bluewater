__pragma__("alias", "S", "$")

class UISession:

    def __init__(self, session):
        self.DOM = lambda: S("#session")
        self.session = session
        self.__initUI()
        self.__bindEvents()

    def __bindEvents(self):
        self.DOM().find('[name="signout"]').click(self.session.logout)
        self.session.eventLogin.append(self.onLogin)
        self.session.eventLogout.append(self.onLogout)

    def onLogin(self):
        self.DOM().removeClass("status-unauthenticated status-authenticated")
        self.DOM().addClass("status-authenticated")

    def onLogout(self):
        self.DOM().removeClass("status-unauthenticated status-authenticated")
        self.DOM().addClass("status-unauthenticated")

    def __initUI(self):
        if firebaseui.auth.AuthUI.getInstance():
            ui = firebaseui.auth.AuthUI.getInstance()
        else:
            ui = __new__(firebaseui.auth.AuthUI(firebase.auth()))

        ui.start('#firebase-login', {
            "callbacks": {
                "signInSuccessWithAuthResult": lambda: False, #self.onSignedIn,
                "signInSuccess": lambda: False, #self.onSignedIn,
            },
            "signInOptions": [
                firebase.auth.GoogleAuthProvider.PROVIDER_ID,
                firebase.auth.GithubAuthProvider.PROVIDER_ID
            ],
        })
