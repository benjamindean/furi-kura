import signal

from .config import Config
from .indicator import FuriKuraIndicator


class FuriKura(object):
    def __init__(self):
        self.config_storage = Config()
        self.ind_inst = FuriKuraIndicator(self.config_storage)

        if not self.config_storage.get_value('access_token'):
            self.handle_login()
        else:
            self.ind_inst.build_menu()

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.ind_inst.main_loop()

    def handle_login(self):
        try:
            import thread
        except ImportError:
            import _thread as thread

        from . import login
        thread.start_new_thread(login.run, ('FuriKura-Login-Server', 1,))
        self.ind_inst.build_login_menu()
