import ctypes
import ctypes.util
import json


class _Options(ctypes.Structure):
    _fields_ = [
        ("cdp", ctypes.c_char_p),
        ("proxy", ctypes.c_char_p),
        ("user_agent", ctypes.c_char_p),
        ("params", ctypes.c_char_p)
    ]


class _Result(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.c_char_p),
        ("err", ctypes.c_char_p),
    ]

    def has_data(self):
        return self.data is not None

    def get_data(self):
        if self.data is not None:
            return self.data.decode('utf8')

        return None

    def has_error(self):
        return self.err is not None

    def get_error(self):
        if self.has_error():
            return self.err.decode('utf8')

        return None


class Error(Exception):
    def __init__(self, query, message):
        self.query = query
        self.message = message


class Ferret:
    def __init__(self, **kwargs):
        self.cdp: str = kwargs.get('cdp', 'http://localhost:9222')
        self.proxy: str = kwargs.get('proxy', '')
        self.user_agent: str = kwargs.get('user_agent', '')
        self.params: dict = kwargs.get('params', {})

        path = '/'.join(__file__.split('/')[:-1])
        self.__ferret = ctypes.CDLL(f'{path}/lib/libferret.so')
        self.__ferret.Execute.restype = _Result

    def execute(self, query: str, **kwargs) -> str:
        opts = _Options(
            cdp=kwargs.get('cdp', self.cdp).encode("utf8"),
            proxy=kwargs.get('proxy', self.proxy).encode("utf8"),
            user_agent=kwargs.get('user_agent', self.user_agent).encode("utf8"),
            params=json.dumps(kwargs.get("params", self.params)).encode("utf8")
        )

        result = self.__ferret.Execute(query.encode("utf8"), opts)

        if result.has_error():
            raise Error(query, result.get_error())

        return result.get_data()

    def execute_json(self, query: str, **kwargs) -> dict:
        resp = self.execute(query, **kwargs)

        return json.loads(resp)
