from .auth.callback import CallbackInfo
from .auth.credientials import Credientials
import urllib.parse  # https://www.urlencoder.io/python/


class OAuth:
    __credientials: Credientials

    def __init__(self, credientials: Credientials):
        self.__credientials = credientials

    def get_oauth_url(self):
        # https://highlevel.stoplight.io/docs/integrations/a04191c0fabf9-authorization
        client_id = self.__credientials.get_client_id()
        redirect_uri = urllib.parse.quote(
            self.__credientials.get_redirect_url())
        scope = ""
        for s in self.__credientials.get_scopes():
            scope = f'{scope} {s}'
        scope = urllib.parse.quote(scope)

        domain = ""
        if self.__credientials.is_white_label():
            domain = 'leadconnectorhq'
        else:
            domain = 'gohighlevel'
        url = f'https://marketplace.{domain}.com/oauth/chooselocation?client_id={client_id}&response_type=code&scope={scope}&redirect_uri={redirect_uri}'
        return url
