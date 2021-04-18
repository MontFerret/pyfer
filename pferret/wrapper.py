import ctypes
import json


class StrReader:
    def __init__(self, script):
        self.__script = script

    def read(self):
        return self.__script


class Ferret:
    def __init__(self, **kwargs):
        self.cdp: str = kwargs.get('cdp', 'http://localhost:9222')
        self.proxy: str = kwargs.get('proxy', '')
        self.user_agent: str = kwargs.get('user_agent', '')
        self.params: dict = kwargs.get('params', {})
        self.__ferret = ctypes.CDLL('../lib/libferret.so')
        self.__ferret.Execute.restype = ctypes.c_char_p

    def execute(self, reader: StrReader, **kwargs) -> str:
        cdp = kwargs.get('cdp', self.cdp)
        proxy = kwargs.get('proxy', self.proxy)
        user_agent = kwargs.get('user_agent', self.user_agent)
        script = reader.read()
        resp = self.__ferret.Execute(script, cdp, proxy, user_agent)
        return resp.decode('utf-8')

    def execute_json(self, reader: StrReader, **kwargs) -> dict:
        resp = self.execute(reader, **kwargs)
        return json.loads(resp)
