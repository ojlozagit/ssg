from enum import Enum

class BlockType(Enum):
    CODE           = "code"
    HEADING        = "heading"
    ORDERED_LIST   = "ordered list"
    PARAGRAPH      = "paragraph"
    QUOTE          = "quote"
    UNORDERED_LIST = "unordered list"