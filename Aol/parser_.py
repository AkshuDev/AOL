import os
import sys

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(__file__))
    sys.path.insert(0, os.getcwd())

import lib
from lib import AOL_LIB
import ErrorHandler
import bin_worker
import settings
from typing_class_handler import *

global vars_

vars_ = {

}

class VarDefineParser():
    def __init__(self, type_:tuple, name:tuple, opr:tuple, value:tuple, line_no:int=0, code:str="", file:str="") -> None:
        self.type_ = type_
        self.name = name
        self.opr = opr
        self.value = value

        self.line_no = line_no
        self.code = code
        self.file = file

        self.settings = settings.configure(os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json"))

    def check(self) -> None:
        if not self.type_ or not self.name or not self.opr or not self.value:
            ErrorHandler.BasicAErrorHandler(line_no=self.line_no, code=self.code, msg="Syntax Error ===> The Variable is not defined properly.", file=self.file)
        else:
            return None

    def write_Var(self, new_var:bool=False) -> None:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "aol_var_dict.aolvd"), "wb") as file:
            pass

    def addVar(self) -> None:
        if self.settings__.VAR_DICT_FILE == "False":
            vars_[self.name] = self.value
        elif self.settings__.VAR_DICT_FILE == "True":
            vars_[self.name] = self.value
        else:
            code = f'"VAR_DICT_FILE": "{self.settings__.VAR_DICT_FILE}"'
            ErrorHandler.BasicAErrorHandler(code=code, specify=True, start_pos=18, end_pos=len(code) - 2, msg="Parser Error: The [VAR_DICT_FILE] key is not set to either [True, False]")

class Parser():
    def __init__(self, tokens:list, log_parse:bool=False, code:str="", file:str="") -> None:
        self.tokens:list = tokens
        self.log_parse:bool = log_parse

        self.line_no:int = 0
        self.line:str = ""
        self.token_id:int = 0
        self.token:tuple = ("", "")

        self.code:str = code
        self.file:str = file

    def calculate(self, nums:list, ops:str) -> int:
        # First pass: handle exponentiation
        i = 0
        while i < len(ops):
            if ops[i] in ["^", "**"]:
                if ops[i] == "^":
                    nums[i] ^= nums[i + 1]
                elif ops[i] == "**":
                    nums[i] **= nums[i + 1]
                nums.pop(i + 1)
                ops.pop(i)
            else:
                i += 1

        # Second pass: handle multiplication, division, floor division, and modulo
        i = 0
        while i < len(ops):
            if ops[i] in ["*", "/", "//", "%"]:
                if ops[i] == "*":
                    nums[i] *= nums[i + 1]
                elif ops[i] == "/":
                    try:
                        nums[i] /= nums[i + 1]
                    except ZeroDivisionError as zde:
                        ErrorHandler.BasicAErrorHandler(line_no=self.line_no, code=self.code, msg=f"DivideByZeroError ===> {zde}.")
                elif ops[i] == "//":
                    nums[i] //= nums[i + 1]
                elif ops[i] == "%":
                    try:
                        nums[i] %= nums[i + 1]
                    except OverflowError as ofe:
                        ErrorHandler.BasicAErrorHandler(line_no=self.line_no, code=self.code, msg=f"OverFlowError ===> {ofe}.")
                nums.pop(i + 1)
                ops.pop(i)
            else:
                i += 1

        # Third pass: handle addition and subtraction
        i = 0
        while i < len(ops):
            if ops[i] == "+":
                nums[i] += nums[i + 1]
            elif ops[i] == "-":
                nums[i] -= nums[i + 1]
            else:
                ErrorHandler.BasicAErrorHandler(line_no=self.line_no, code=self.code, msg=f"Syntax Error ===> No such operation [{ops[i]}]", file=self.file)
            nums.pop(i + 1)
            ops.pop(i)

        return nums[0]

    def parse(self) -> None:
        for line_no, line in enumerate(self.tokens):
            self.line_no = line_no
            self.line = line

            nums = []
            ops = []

            for token_id, token in enumerate(line):
                self.token_id = token_id
                self.token = token

                type_ = token[0]
                char = token[1]

                if type_ == AOL_LIB.int or type_ in AOL_LIB.avail_oprs_type_:
                    if type_ == AOL_LIB.int:
                        nums.append(int(char))
                    else:
                        ops.append(char)

            if not len(nums) == 0 and not len(ops) == 0:
                if len(nums) == len(ops) + 1:
                    result = self.calculate(nums, ops)

                    if self.log_parse:
                        print(f"LINE==> {self.code.splitlines()[self.line_no]}\nRESULT:", result)
                else:
                    ErrorHandler.BasicAErrorHandler(line_no=self.line_no, code=self.code, msg="Syntax Error ===> This calculation is invalid.", file=self.file)