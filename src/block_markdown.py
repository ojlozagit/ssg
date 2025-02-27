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