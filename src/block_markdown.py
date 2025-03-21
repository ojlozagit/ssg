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
@return: associated block type of input block
'''
def block_to_block_type(markdown):
    lines = markdown.split("\n")

    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ",
                            "###### ")):
        return BlockType.HEADING
    if( len(lines) > 1
    and markdown.startswith("```")
    and markdown.endswith("```") ):
        return BlockType.CODE
    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if markdown.startswith("1. "):
        for idx, line in enumerate(lines):
            if not line.startswith(f"{idx + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.OLIST

    return BlockType.PARAGRAPH