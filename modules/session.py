from modules.builders import user_builder

class Session:

    def __init__(self):
        self.user = None

    def set_user(self, login):
        builder = user_builder.UserBuilder.get_user()
        self.user = builder.from_login(login).build()
        return self.user is not None

    def get_user(self):
        return self.user
