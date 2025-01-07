import time

from utils.settings import (
    GlobalConditionVariables,
    MutableSharedSettings,
    get_MOUSE_LISTEN_KEEP_GOING,
    set_MOUSE_LISTEN_KEEP_GOING,
)


def clickFunc(self):
    self.hide()
    set_MOUSE_LISTEN_KEEP_GOING(True)
    MutableSharedSettings.POP_BUTTON = False
    with GlobalConditionVariables.CV_BUTTON_KEY_LISTEN:
        GlobalConditionVariables.CV_BUTTON_KEY_LISTEN.notify_all()
    if self.parent.isHidden() or self.parent.isMinimized():
        time.sleep(0.3)  # wait for copy operation
        self.parent.moveToMousePosition()
