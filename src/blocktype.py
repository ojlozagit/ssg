from enum import Enum

class BlockType(Enum):
    CODE      = "code"
    HEADING   = "heading"
    OLIST     = "ordered list"
    PARAGRAPH = "paragraph"
    QUOTE     = "quote"
    ULIST     = "unordered list"