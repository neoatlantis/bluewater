from .ui.session import UISession
from .ui.mainkey import UIMainkey

class UI:

    def __init__(self, session, mainkey):
        self.ui = {
            "session": UISession(session),
            "mainkey": UIMainkey(mainkey),
        }
