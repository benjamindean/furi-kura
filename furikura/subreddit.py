from .utils import get_file


class SubredditChooser(object):
    def __init__(self, config_storage, builder):
        self.config_storage = config_storage
        self.builder = builder
        self.config = self.config_storage.config
        self.builder.add_from_file(get_file('furikura/ui/subreddit.xml'))
        self.chooser = self.builder.get_object('choose_subreddit')

    def show_window(self):
        subreddit_name = self.builder.get_object('subreddit_name')
        posts_type = self.builder.get_object('posts_type')
        posts_limit = self.builder.get_object('posts_limit')

        subreddit_name.set_text(self.config.get('subreddit', 'No Subreddit'))
        posts_type.set_active_id(self.config.get('posts_type', '1'))
        posts_limit.set_active_id(self.config.get('posts_limit', '5'))

        save = self.builder.get_object('save')
        cancel = self.builder.get_object('cancel')

        cancel.connect('clicked', self.__chooser_destroy)
        save.connect('clicked', self.__chooser_save, (subreddit_name, posts_type, posts_limit))

        self.chooser.show()

    def __chooser_destroy(self, *args):
        self.chooser.destroy()

    def __chooser_save(self, widget, data):
        subreddit_name = data[0].get_text()
        posts_type = data[1].get_active_id()
        posts_limit = data[2].get_active_id()

        self.config_storage.set_key('subreddit', subreddit_name)
        self.config_storage.set_key('posts_type', posts_type)
        self.config_storage.set_key('posts_limit', posts_limit)

        self.__chooser_destroy()
