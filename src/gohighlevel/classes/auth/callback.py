class CallbackInfo:
    __code: str = ""
    __refres_token: str = ""

    def __init__(self, code, refres_token):
        self.__code = code
        self.__refres_token = refres_token

    def get_code(self):
        return self.__code

    def get_refres_token(self):
        return self.__refres_token
