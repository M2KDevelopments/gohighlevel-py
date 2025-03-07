class Credientials:
    __client_id: str = ""
    __client_secret: str = ""
    __redirect_url: str = ""
    __scopes: [] = []
    __is_white_label: str = ""

    def __init__(self, client_id, client_secret, redirect_url, scopes, is_white_label):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__redirect_url = redirect_url
        self.__scopes = scopes
        self.__is_white_label = is_white_label

    def get_redirect_url(self):
        return self.__redirect_url

    def get_client_id(self):
        return self.__client_id

    def get_client_secret(self):
        repr = self.__client_secret

    def is_white_label(self):
        return self.__is_white_label

    def get_scopes(self):
        return self.__scopes
