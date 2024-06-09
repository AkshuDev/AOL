import os
import sys
import math
import binascii
from typing import *
from PheonixAppAPI import (api, main)

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(__file__))
    sys.path.insert(0, os.getcwd())

PAapi_parent = main.PheonixAppAPI(False).initialize()
api.set_parent(PAapi_parent)

import lib
from lib import AOL_LIB

import ErrorHandler

class BIN():
    def __init__(self, path:str="./aol_var-dict.aolvd", format:str="vardict-v0.001JSON", encoding:str="utf-8", encode:bool=False, content:str="", content_dict:dict={}, use_base64:bool=False, use_pheonixApp_encoder:bool=False) -> None:
        self.path = path
        if not os.path.exists(self.path):
            pass

        self.format:str = format
        self.encoding:str = encoding
        self.encode:bool = encode
        self.content:str = content
        self.content_dict :dict= content_dict
        self.use_base64:bool = use_base64
        self.use_pheonixapp_encoder:bool = use_pheonixApp_encoder

    def bin_to_str(self, data:Union[str, int]) -> str:
        data = str(data)

        l=[]
        m=""
        for i in data:
            b=0
            c=0
            k=int(math.log10(i))+1
            for j in range(k):
                b=((i%10)*(2**j))
                i=i//10
                c=c+b
                l.append(c)
        for x in l:
            m=m+chr(x)
        return m

    def str_to_bytes(self, data, encoding:str="utf-8") -> bytes:
        return bytes(str(data), encoding)

    def to_binINT(self, data_dict:dict={}, data_str:str="", useString:bool=True) -> int:
        l,m = []

        dict_str:str = ""

        if useString:
            for i in data_str:
                l.append(ord(i))

            for i in l:
                m.append(int(bin(i)[2:]))

            return m
        else:
            dict_str = str(data_dict)

            for i in data_str:
                l.append(ord(i))

            for i in l:
                m.append(int(bin(i)[2:]))

            return m

    def push_str(self) -> None:
        data = api.Encoder(self.content, "Hype_Space").Encode()

        with open(self.path, "wb") as file:
            file.write(self.str_to_bytes(data))

BIN("./test.bin", "none", encoding="utf-16", encode=True, content="Hello World!!").push_str()