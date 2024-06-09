import os
import sys

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(__file__))

print(os.getcwd())

import lexer as lex
import parser_ as parser

if len(sys.argv) == 1:
    while True:
        shell = input(f"{os.getcwd()}\tAOL$>>>\n")

        if "exit(" in shell and ")" in shell:
            exit(shell[5])

        toks = lex.Lexer(shell).tokenize()

        print(toks)

        parser.Parser(toks, True, shell).parse()
else:
    with open(sys.argv[1], "r") as f:
        code = f.read()

    toks = lex.Lexer(code, "./test.aol").tokenize()

    print(toks)

    parser.Parser(toks, True, code, "./test.aol").parse()