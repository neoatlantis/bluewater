__pragma__("alias", "S", "$")

from .session import Session
from .ui import UI 

def main():
    ui = UI(
        Session()
    )

S(main)
