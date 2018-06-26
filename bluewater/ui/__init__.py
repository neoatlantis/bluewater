from .ui.session import UISession

class UI:

    def __init__(self, session):
        self.ui = {
            "session": UISession(session)
        }
