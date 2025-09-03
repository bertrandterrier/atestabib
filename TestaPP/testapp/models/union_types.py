from typing import Union

from item import Signature
from member import MemberData, MemberReg
from bookcase import BookCaseAddr, BookCase, Route, RouteReg

RegType = Union[MemberReg, RouteReg]
TokenType = Union[MemberData, Signature, BookCaseAddr, BookCase, Route]
TaType = Union[MemberReg, RouteReg, MemberData, Signature, BookCaseAddr, BookCase, Route] 
