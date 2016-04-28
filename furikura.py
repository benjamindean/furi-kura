from furikura import config
from furikura import indicator


class FuriKura:
    def __init__(self):
        print("Init main")
        config_storage = config.Config()
        ind_inst = indicator.FuriKuraIndicator(config_storage)

        if not config_storage.get_key("access_token"):

            from furikura import login
            import thread

            thread.start_new_thread(login.run, ("FuriKura-Login-Server", 1,))
            ind_inst.build_login_menu()
        else:
            ind_inst.build_menu()

        ind_inst.main_loop()


if __name__ == '__main__':
    FuriKura()
