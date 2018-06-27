__pragma__("alias", "S", "$")

from .session import Session
from .mainkey import Mainkey

from .ui import UI 

def main():
    session = Session()
    mainkey = Mainkey(session)

    ui = UI(session, mainkey)


S(main)
