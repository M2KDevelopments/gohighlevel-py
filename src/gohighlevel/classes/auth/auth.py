class AuthHeader:
    Version = "2021-04-15"
    Authorization = "",
    Accept = 'application/json'

    def __init__(self, access_token: str):
        self.Authorization = f'Bearer {access_token}'

    def get_headers(self):
        return {
            'Version': self.Version,
            'Authorization': self.Authorization,
            'Accept': self.Accept
        }


class AuthData:
    __access_token: str
    __location_id: str
    __company_id: str
    __refresh_token: str
    __expires_in: int
    __user_type: str
    __use_api_key: str
    __scope: str  # "Company" | "Location"
    __headers: AuthHeader

    def __init__(self, access_token: str, location_id: str, company_id: str, refresh_token: str, expires_in: int, user_type: str, use_api_key: bool, scope, headers: AuthHeader):
        self.__access_token = access_token
        self.__location_id = location_id
        self.__company_id = company_id
        self.__refresh_token = refresh_token
        self.__expires_in = expires_in
        self.__user_type = user_type
        self.__use_api_key = use_api_key
        self.__scope = scope
        if (headers is None):
            self.__headers = AuthHeader(access_token)
        else:
            self.__headers = headers

    def get_auth(self):
        return {
            "access_token": self.__access_token,
            "location_id": self.__location_id,
            "company_id": self.__company_id,
            "refresh_token": self.__refresh_token,
            "expires_in": self.__expires_in,
            "user_type": self.__user_type,
            "use_api_key": self.__use_api_key,
            "scope": self.__scope,  # "Company" | "Location"
            "headers": self.__headers.get_headers(),
        }
