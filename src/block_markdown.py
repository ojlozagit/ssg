from blocktype import *
'''
@markdown: raw string (representing a full document)
@return: list of "block" strings
'''
def markdown_to_blocks(markdown):
    blocks = []
    split_md = markdown.split("\n\n")

    for block in split_md:
        if block == "":
            continue
        blocks.append(block.strip())

    return blocks

'''
@markdown: single block of raw markdown text
'''
def block_to_block_type(markdown):
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ",
                            "###### ")):
        return BlockType.HEADING
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    if markdown.startswith(">"):
        return BlockType.QUOTE
    if markdown.startswith("- "):
        ul = markdown.split("\n")
        for line in ul:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if markdown.startswith("1. "):
        seq = 1
        ol = markdown.split("\n")
        for line in ol:
            if not line.startswith(f"{seq}."):
                return BlockType.PARAGRAPH
            seq += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH