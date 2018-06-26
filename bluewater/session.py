from .event import Event

class Session:

    def __init__(self):
        self.__bindEvents()

    def __bindEvents(self):
        self.eventLogin = Event()
        self.eventLogout = Event()
        firebase.auth().onAuthStateChanged(self.onAuthStateChanged)

    def onAuthStateChanged(self):
        if self.getCurrentUser():
            console.log("Event: login")
            self.eventLogin.call()
        else:
            console.log("Event: logout")
            self.eventLogout.call()
        
    def getCurrentUser(self):
        return firebase.auth().currentUser

    async def logout(self):
        console.log("Log user out.")
        firebase.auth().signOut()
