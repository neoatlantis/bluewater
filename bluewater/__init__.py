__pragma__("alias", "S", "$")

from .session import Session
from .mainkey import Mainkey
from .entries import Entries

from .ui import UI 

def main():
    session = Session()
    mainkey = Mainkey(session)
    entries = Entries(mainkey)

    ui = UI(session, mainkey)


S(main)
