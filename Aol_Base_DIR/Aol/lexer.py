import os
import sys

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(__file__))
    sys.path.insert(0, os.getcwd())

import lib
from lib import AOL_LIB

import ErrorHandler

class Lexer():
    def __init__(self, code:str, file:str="") -> None:
        self.code:str = code
        self.file:str = file
        self.current_line:str = ""
        self.line:str = ""
        self.lines:str = ""
        try:
            self.lines = self.code.splitlines()
            self.line = self.lines[0]
        except Exception:
            ErrorHandler.BasicAExceptionHandler(line_no=0, code="[EOF]", msg="File Contains no code", file=file)
        self.current_char:str = ""
        self.current_char_no:int = 0
        self.line_no:int = 0

    def string_(self) -> tuple[str, int, bool]:
        string = ""
        is_string = False
        quote = "'"
        quote2 = '"'

        while self.current_char_no < len(self.line):
            self.current_char = self.line[self.current_char_no]
            if self.current_char == quote or self.current_char == quote2:
                if is_string:
                    if self.current_char_no < len(self.line) - 1:
                        self.advance()
                        break
                    else:
                        break
                else:
                    if self.current_char_no < len(self.line) - 1:
                        self.advance()
                        is_string = True

            elif self.current_char_no == len(self.line) - 1 and is_string:
                ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Syntax Error ==> The string was not closed.", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)

            if is_string:
                string += self.current_char

            if self.current_char_no < len(self.line) - 1:
                self.advance()
            else:
                break

        return string, self.current_char_no, True

    def int_(self) -> tuple[str, int]:
        integer = ""

        while self.current_char_no < len(self.line) and self.line[self.current_char_no].isdigit():
            integer += self.current_char
            if self.current_char_no < len(self.line) - 1:
                self.advance()
            else:
                break

        return integer, self.current_char_no

    def double(self) -> tuple[str, int]:
        double = ""
        seen_dot = False

        while self.current_char_no < len(self.line) and (self.current_char.isdigit() or (self.current_char == '.')):
            if self.current_char == '.':
                seen_dot = True
            double += self.current_char
            if self.current_char_no < len(self.line) - 1:
                self.advance()
            else:
                break

        return double, self.current_char_no

    def int_double_check(self) -> tuple[str, int, str]:
        start_pos = self.current_char_no
        checker = ""

        while self.current_char_no < len(self.line) and self.line[self.current_char_no].isdigit() or self.line[self.current_char_no] == "." and self.current_char_no < len(self.line):
            checker += self.line[self.current_char_no]
            if self.current_char_no < len(self.line) - 1:
                self.advance()
            else:
                break

        if "." in checker:
            self.advance(i=start_pos, v=self.line[start_pos], do=True)
            double, skip_to = self.double()
            return double, skip_to, AOL_LIB.double
        else:
            self.advance(i=start_pos, v=self.line[start_pos], do=True)
            int_, skip_to = self.int_()
            return int_, skip_to, AOL_LIB.int

    def digit_opr_check(self) -> tuple[str, int, str]:
        val = ""
        val2 = ""
        skip_to = 0

        if self.current_char in "+-":
            val = self.current_char

            if self.current_char_no < len(self.line) - 1:
                self.advance()
                if self.current_char.isdigit():
                    # Check if it's part of a number
                    number, skip_to, type_ = self.int_double_check()
                    val += number
                    return val, skip_to, type_
                else:
                    # It's an operator
                    val2 = AOL_LIB.plus if val == "+" else AOL_LIB.minus
                    return val, skip_to, val2
            else:
                ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Syntax Error ==> Operator at end of line", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)

        # If it's a number
        val3, skip_to, type_ = self.int_double_check()
        val += val3
        return val, skip_to, type_

    def getAlphas(self) -> tuple[str, int]:
        alphas = ""

        while self.current_char_no < len(self.line):
            if self.current_char.isalpha():
                alphas += self.current_char

                if self.current_char_no < len(self.line) - 1:
                    self.advance()
                else:
                    break
            else:
                break

        return alphas, self.current_char_no

    def advance(self, steps:int=1, i:int=0, v:str="", do:bool=False) -> None:
        if not do:
            self.current_char_no += steps
        else:
            self.current_char_no = i
        if not do:
            self.current_char = self.line[self.current_char_no] if self.line else ''
        else:
            self.current_char = v

    def tokenize(self) -> list:
        tokens:list = []
        line_tokens:list = []
        wpmiem_timer:int = 0
        self.current_char_no = 0
        self.line_no = 0
        var_finder = ""

        while self.line_no < len(self.lines):
            if self.line_no >= len(self.lines):
                break

            self.line = self.lines[self.line_no]
            self.current_char_no = 0

            while self.current_char_no < len(self.line):
                if self.current_char_no > len(self.line) - 1:
                    break

                self.current_char = self.line[self.current_char_no]

                if  self.current_char_no  == len(self.line) - 1:
                    if self.current_char == ";":
                        if wpmiem_timer == 0:
                            wpmiem_timer = 1
                        else:
                            wpmiem_timer = 0
                            break
                    else:
                        ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Syntax Error ==> Line is not closed by [;]", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)

                if self.current_char == ";":
                    if self.current_char_no == len(self.line) - 1:
                        break
                    else:
                        ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Synatx Error ==> [;] is not at the end of the line.", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)

                if self.current_char.isspace():
                    if not self.current_char_no >= len(self.line):
                        if self.current_char_no < len(self.line) - 1:
                            self.advance()
                        else:
                            break
                    else:
                        break
                    continue

                elif (self.current_char.isdigit() or self.current_char in "+-") and not self.current_char_no == len(self.line) - 1:
                    if self.current_char in "+-":
                        val, skip_to, type_ = self.digit_opr_check()
                        tokens.append((type_, val))
                    elif self.current_char.isdigit():
                        val, skip_to, type_ = self.int_double_check()
                        tokens.append((type_, val))
                    continue

                elif self.current_char == "'" or self.current_char == '"':
                    if not self.current_char_no == len(self.line) - 1:
                        string_, skip_to, do = self.string_()
                        if do:
                            tokens.append((AOL_LIB.str, string_))
                            continue
                        continue
                    else:
                        if self.current_char_no < len(self.line) - 1:
                            self.advance()
                            continue
                        else:
                            break
                    continue

                elif self.current_char == "/":
                    if self.current_char_no != len(self.line) - 2:
                        if self.line[self.current_char_no + 1] != "/":
                            tokens.append((AOL_LIB.div, "/"))
                        else:
                            tokens.append((AOL_LIB.flrdiv, "//"))
                            self.advance()
                    else:
                        ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Synatx Error ==> Operator at the end of line.", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)
                elif self.current_char == "*":
                    if self.current_char_no != len(self.line) - 2:
                        if self.line[self.current_char_no + 1] != "*":
                            tokens.append((AOL_LIB.mult, "*"))
                        else:
                            tokens.append((AOL_LIB.pwr, "**"))
                            self.advance()
                    else:
                        ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Synatx Error ==> Operator at the end of line.", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)
                elif self.current_char == "(":
                    if self.current_char_no != len(self.line) - 2:
                        tokens.append((AOL_LIB.lpar, "("))
                    else:
                        ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Synatx Error ==> Operator at the end of line.", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)
                elif self.current_char == ")":
                    if self.current_char_no != len(self.line) - 2:
                        tokens.append((AOL_LIB.rpar, ")"))
                    else:
                        ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Synatx Error ==> Operator at the end of line.", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)
                elif self.current_char == "%":
                    if self.current_char_no != len(self.line):
                        tokens.append((AOL_LIB.divi, "%"))
                    else:
                        ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Synatx Error ==> Operator at the end of line.", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)
                elif self.current_char == "^":
                    if self.current_char_no != len(self.line) - 2:
                        tokens.append((AOL_LIB.xor, "^"))
                    else:
                        ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Synatx Error ==> Operator at the end of line.", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)

                elif self.current_char == "=":
                    if self.current_char_no < len(self.line) - 1:
                        self.advance()
                    else:
                        ErrorHandler.BasicAExceptionHandler(line_no=self.line_no, code=self.code, msg="Synatx Error ==> Operator at the end of line.", file=self.file, specify=True, start_pos=self.current_char_no, end_pos=self.current_char_no)

                    if self.current_char == "=":
                        tokens.append((AOL_LIB.equals, self.current_char))
                    else:
                        tokens.append((AOL_LIB.asign,  self.line[self.current_char_no - 1]))

                elif self.current_char.isalpha():
                    alphas, skipTo = self.getAlphas()
                    if alphas == "var":
                        tokens.append((AOL_LIB.var, alphas))
                    elif alphas == "int":
                        tokens.append((AOL_LIB.DTint, alphas))
                    elif alphas == "double":
                        tokens.append((AOL_LIB.DTdouble, alphas))
                    elif alphas == "char":
                        tokens.append((AOL_LIB.DTchar, alphas))
                    elif alphas == "str":
                        tokens.append((AOL_LIB.DTstr, alphas))
                    elif alphas == "bool":
                        tokens.append((AOL_LIB.DTbool, alphas))
                    elif alphas == "func":
                        tokens.append((AOL_LIB.DTfunc, alphas))
                    elif alphas == "obj":
                        tokens.append((AOL_LIB.DTobj, alphas))
                    else:
                        tokens.append((AOL_LIB.varname, alphas))

                if not self.current_char_no >= len(self.line) - 1:
                    self.advance()
                else:
                    break

            self.line_no += 1
            line_tokens.append(tokens)
            tokens = []

        return line_tokens