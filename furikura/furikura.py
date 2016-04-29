from .config import Config
from .indicator import FuriKuraIndicator


class FuriKura(object):
    def __init__(self):
        print("Init main")
        config_storage = Config()
        ind_inst = FuriKuraIndicator(config_storage)

        if not config_storage.get_value("access_token"):
            import thread
            from . import login
            thread.start_new_thread(login.run, ("FuriKura-Login-Server", 1,))
            ind_inst.build_login_menu()
        else:
            ind_inst.build_menu()

        ind_inst.main_loop()
