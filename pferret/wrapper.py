import ctypes
import ctypes.util
import json


class StrReader:
    def __init__(self, script):
        self.__script = script

    def read(self):
        return self.__script


class Options(ctypes.Structure):
    _fields_ = [
        ("cdp", ctypes.c_char_p),
        ("proxy", ctypes.c_char_p),
        ("user_agent", ctypes.c_char_p)
    ]


class Result(ctypes.Structure):
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
    def __init__(self, script, message):
        self.script = script
        self.message = message


class Ferret:
    def __init__(self, **kwargs):
        self.cdp: str = kwargs.get('cdp', 'http://localhost:9222')
        self.proxy: str = kwargs.get('proxy', '')
        self.user_agent: str = kwargs.get('user_agent', '')
        self.params: dict = kwargs.get('params', {})
        path = '/'.join(__file__.split('/')[:-1])
        self.__ferret = ctypes.CDLL(f'{path}/lib/libferret.so')
        self.__ferret.Execute.restype = Result

    def execute(self, reader: StrReader, **kwargs) -> str:
        opts = Options(
            cdp=ctypes.c_char_p(kwargs.get('cdp', self.cdp).encode("utf8")),
            proxy=ctypes.c_char_p(kwargs.get('proxy', self.proxy).encode("utf8")),
            user_agent=ctypes.c_char_p(kwargs.get('user_agent', self.user_agent).encode("utf8"))
        )

        script = reader.read()
        result = self.__ferret.Execute(script, opts)

        if result.has_error():
            raise Error(script, result.get_error())

        print(result.get_data())

        return result.get_data()

    def execute_json(self, reader: StrReader, **kwargs) -> dict:
        resp = self.execute(reader, **kwargs)

        return json.loads(resp)
