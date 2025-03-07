import classes.auth.auth as Auth
import classes.auth.credientials as Credientials
import classes.oauth as OAuth

PROD = "https://services.leadconnectorhq.com"
MOCK = "https://stoplight.io/mocks/highlevel/integrations/39582850"


class GoHighlevel:

    __BASEURL = 'https://services.leadconnectorhq.com'
    __authData: Auth.AuthData

    credientials: Credientials.Credientials
    oauth: OAuth.OAuth

    def __init__(self, credientials: Credientials.Credientials):
        self.credientials = credientials
        self.oauth = OAuth.OAuth(credientials)

    def set_auth(self, auth: Auth.AuthData):
        self.__authData = auth

    def setTestMode(self, test: bool):
        if test is True:
            self.__BASEURL = MOCK
        else:
            self.__BASEURL = PROD