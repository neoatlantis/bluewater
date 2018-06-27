from .event import Event

class Entries:

    def __init__(self, mainkey):
        self.session = mainkey.session
        self.mainkey = mainkey
        self.__bindEvents()

    def __bindEvents(self):
        self.eventEntryAdded = Event()
        self.mainkey.eventDecrypted.append(self.onDecrypted)

    async def onDecrypted(self):
        self.path = "/{}/".format(self.session.getCurrentUser().uid)
        ref = firebase.database().ref(self.path)
        ref.on("child_added", self.onEntryAdded)
        ref.on("child_changed", self.onEntryChanged)
        ref.on("child_removed", self.onEntryRemoved)

    async def onLogout(self):
        firebase.database().ref(self.path).off()

    async def onEntryAdded(self, data):
        if data.key == self.mainkey.FIREBASE_MAINKEY: return
        console.log(data.val(), data.key)

    async def onEntryChanged(self, data):
        if data.key == self.mainkey.FIREBASE_MAINKEY: return
        pass

    async def onEntryRemoved(self, data):
        if data.key == self.mainkey.FIREBASE_MAINKEY: return
        pass
