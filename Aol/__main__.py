import os
import sys
import atexit
import platform
from typing_class_handler import *

global data

data = os.getcwd()

global code
code:str = ""

if len(sys.argv) >= 2:
    if sys.argv[1] != "-u":
        with open(sys.argv[1], "r") as f:
            code = f.read()

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(__file__))

print("Running on", os.getcwd())

import lexer as lex
import parser_ as parser
import settings

settings_ = settings.configure("settings.json")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        while True:
            shell = input(f"{os.getcwd()}\tAOL$>>>\n")

            if "exit(" in shell and ")" in shell:
                exit(shell[5])

            toks = lex.Lexer(shell).tokenize()

            print(toks)

            parser.Parser(toks, True, shell).parse()
    else:
        if code != "":
            toks = lex.Lexer(code, "./test.aol").tokenize()

            print(toks)

            parser.Parser(toks, True, code, "./test.aol").parse()
        else:
            if len(sys.argv) > 2:
                if sys.argv[2] == "build":
                    if len(sys.argv) > 3:
                        if sys.argv[3] == "addon":
                            if len(sys.argv) > 6:
                                addon_name = sys.argv[4]
                                addon_path = sys.argv[5]
                                settings.Builder(sys.argv[6], settings_).build_addon(addon_path, addon_name)
                            elif len(sys.argv) > 5:
                                addon_name = sys.argv[4]
                                addon_path = sys.argv[5]
                                settings.Builder(settings_.DEFAULT_OUTPUT_DIR, settings_).build_addon(addon_path, addon_name)
                            else:
                                raise RuntimeError("Not Enough specifications.")
                        elif sys.argv[3] == "module":
                            if len(sys.argv) > 6:
                                print(sys.argv)
                                module_name = sys.argv[4]
                                module_path = sys.argv[5]
                                settings.Builder(sys.argv[6], settings_).build_module(module_path, module_name)
                            elif len(sys.argv) > 5:
                                module_name = sys.argv[4]
                                module_path = sys.argv[5]
                                settings.Builder(settings_.DEFAULT_OUTPUT_DIR, settings_).build_module(module_path, module_name)
                            else:
                                raise RuntimeError("Not Enough specifications.")
                        else:
                            raise RuntimeError(f"AOL Error: No such type [{sys.argv[3]}]")
                    else:
                        raise RuntimeError("AOL Error: Nothing Specified after 'build'")
            else:
                raise RuntimeError("AOL Error: Nothing Specified after '-u'")
else:
    raise RuntimeError("AOL Error: Aol module is required to start within the terminal to work else the code terminates.")