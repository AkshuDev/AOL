import os
import sys

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(__file__))

class _Error_():
    def __init__(self) -> None:
        pass

    def Exception_(self, msg:str="", line_no:int=0, code:str="", file:str="", specifier:str="^", specify:bool=False, start_pos:int=0,
    end_pos:int=0) -> None:
        specifier_str = ""
        start = False
        if specify:
            idx = 0
            while idx <= len(code.splitlines()[line_no]) - 1:
                if idx == start_pos:
                    start = True

                if start:
                    specifier_str += specifier
                else:
                    specifier_str += " "

                if idx == end_pos:
                    start = False
                    break
                idx += 1

        file_msg = f"at FILE: [{file}]"
        if file == "":
            file_msg = ""

        code_lines = ""
        i = line_no
        id = 3

        while not i == 0 and not id == 0:
            code_lines += f"{code.splitlines()[line_no - i]}\n"
            i -= 1
            id -= 1

        code_lines += code.splitlines()[line_no]

        msg = f"""Traceback for Exception: A Error Occurred during the handling of line no [{line_no}] {file_msg}
{code_lines}

LINE =>
{code.splitlines()[line_no]}
{specifier_str}


Error: {msg}"""

        return msg

    def ParserError(self, msg:str="", line_no:int=0, code:str="", file:str="") -> str:
        file_msg = f"at FILE: [{file}]"
        if file == "":
            file_msg = ""

        code_lines = ""
        i = line_no - 1
        id = 3

        while not i == 0 and not id == 0:
            code_lines += f"{code.splitlines()[line_no - i]}\n"
            i -= 1
            id -= 1

        code_lines += code.splitlines()[line_no]

        msg = f"""Traceback for ParserError: A Error Occurred during the handling of line no [{line_no}] {file_msg}
{code_lines}

LINE =>
{code.splitlines()[line_no]}

ParserError: {msg}"""

        return msg

    def InternalError(self, msg:str="", line_no:int=0, code:str="", file:str="") -> str:
        file_msg = f"at FILE: [{file}]"
        if file == "":
            file_msg = ""

        code_lines = ""
        i = line_no - 1
        id = 3

        while not i == 0 and not id == 0:
            code_lines += f"{code.splitlines()[line_no - i]}\n"
            i -= 1
            id -= 1

        code_lines += code.splitlines()[line_no]

        msg = f"""Traceback for InternalError: A Error Occurred during the handling of line no [{line_no}] {file_msg}
{code_lines}

LINE =>
{code.splitlines()[line_no]}

InternalError: {msg}"""

        return msg

class BasicAExceptionHandler():
    def __init__(self, Error:str=_Error_().Exception_, line_no:int=1, code:str="", msg:str="", file:str="", specifier:str="^", specify:bool=False, start_pos:int=0, end_pos:int=0) -> None:
        self.Error = Error
        self.code = code
        self.line_no = line_no
        self.msg = msg

        print(self.Error(self.msg, self.line_no, self.code, os.path.abspath(file), specifier, specify, start_pos, end_pos))
        exit(1)

class BasicAErrorHandler():
    def __init__(self, Error:str=_Error_().ParserError, line_no:int=0, code:str="", msg:str="", file:str="") -> None:
        self.Error = Error
        self.code = code
        self.line_no = line_no
        self.msg = msg
        self.file = file

        print(self.Error(msg, line_no, code, os.path.abspath(file)))
        exit(1)