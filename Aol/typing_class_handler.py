import os
import typing
import sys

if __name__ == '__main__':
    print("Sorry, this is a private class. No user can use this. Bye :)")
    exit(1)

# Define new types using typing.NewType
FileOrString = typing.NewType('FileOrString', typing.Union[str, os.PathLike])
DirectoryOrString = typing.NewType('DirectoryOrString', typing.Union[str, os.PathLike])
URL = typing.NewType('URL', str)

# Generic types for Encodable and Decodable
T = typing.TypeVar('T')

class Encodable(typing.Generic[typing.TypeVar('T')]):
    """Base class for data types that can be encoded to a string or bytes."""
    pass


class Decodable(typing.Generic[typing.TypeVar('T')]):
    """Base class for data types that can be decoded from a string or bytes."""
    pass
