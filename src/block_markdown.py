import re

from textnode        import *
from htmlnode        import ParentNode
from blocktype       import BlockType
from inline_markdown import text_to_textnodes
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
    if markdown.startswith(("- ", "* ", "+ ")):
        for line in lines:
            if not line.startswith(("- ", "* ", "+ ")):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if markdown.startswith("1. "):
        for idx, line in enumerate(lines):
            if not line.startswith(f"{idx + 1}. "):
                return BlockType.PARAGRAPH
        return BlockType.OLIST

    return BlockType.PARAGRAPH

'''
@markdown: full markdown document
@return: single parent HTMLNode
'''
def markdown_to_html_node(markdown):
    block_nodes = []
    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        # Temporary conditional to help with VSCode intelisense
        if not isinstance(block, str):
            raise Exception("markdown_to_blocks failed")

        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                p_block = " ".join(block.split()).replace("\n", " ")
                children = text_to_children(p_block)
                block_nodes.append(ParentNode("p", children))

            case BlockType.HEADING:
            # - Markdown: Headings start with one or more #
            #   characters followed by a space, e.g., # Heading 1 or
            #   ### Heading 3.
            # - HTML: These map to <h1> through <h6> tags based on
            #   the number of # characters.
            # - Key Rules:
            #   - Trailing whitespace should be trimmed, as it is not
            #     part of the heading.
            #   - Headings generally do not preserve internal
            #     excessive spaces (e.g., # A Heading becomes
            #     <h1>A Heading).
            #   - Heading content may include inline formatting such
            #     as bold (**), italic (_), or links, which must also
            #     be parsed.
                h_count = block.find(" ")
                h_block = block.removeprefix("#" * h_count + " " )
                h_block = " ".join(h_block.split()).replace("\n", " ")

                h_tag = f"h{h_count}"
                children = text_to_children(h_block)
                block_nodes.append(ParentNode(h_tag, children))

            case BlockType.QUOTE:
            # - Markdown: Lines prefixed with a > followed by a space
            #   form a quote block. For example, > Quoted text.
            # - HTML: Wrap content in a <blockquote> tag.
            # - Key Rules:
            #   - Multiple consecutive lines prefixed with > are
            #     treated as part of the same quote block, where the
            #     "> " is stripped, and newlines are replaced with a
            #     single space.
            #   - Single blank lines between > lines end one quote
            #     block and start another.
            #   - Inline formatting still applies inside the quoted
            #     text (e.g., > **Bold quote** becomes
            #     <blockquote><b>Bold quote</b></blockquote>).
                block_lines = block.split("\n")
                block_lines = list(map(lambda line: line[1:],
                                       block_lines))
                q_block = " ".join(" ".join(block_lines).split())

                children = text_to_children(q_block)
                block_nodes.append(ParentNode("blockquote", children))

            case BlockType.OLIST:
            # - Markdown: Lines starting with numbers followed by a
            #   period and a space, e.g., 1. Item 1, 2. Item 2.
            # - HTML: Map to an <ol> tag, with each list item inside
            #   an <li>.
            # - Key Rules:
            #   - Line breaks/newlines within the list are ignored if
            #     the lines are part of the same logical list.
            #   - Items may contain inline formatting, which must be
            #     parsed (e.g., 1. **Bold Item** becomes
            #     <b>Bold Item</b> inside the <li>).
            #   - Preserve the order of items, as 2. Item should
            #     remain the second item.
                lst_itms = block.split("\n")
                ol_pattern = re.compile(r"\d+\. ")
                lst_itms = list(map(lambda itm: re.sub(ol_pattern,
                                                       "", itm, 1),
                                    lst_itms))
                lst_children = []
                for text in lst_itms:
                    children = text_to_children(text)
                    lst_children.append(ParentNode("li", children))
                block_nodes.append(ParentNode("ol", lst_children))

            case BlockType.ULIST:
            # - Markdown: Lines starting with -, *, or + followed by
            #   a space, e.g., - Item 1, * Item 2.
            # - HTML: Map to a <ul>, with each item wrapped in an
            #   <li>.
            # - Key Rules:
            #   - Line breaks/newlines within the list are treated
            #     similarly to ordered lists—ignored if logically
            #     part of the same list.
            #   - Like ordered lists, each list item may include
            #     inline formatting (_italic_, **bold**, etc.) that
            #     needs processing.
            #   - Consistency of the bullet symbol (-, *, or +)
            #     doesn't matter—they're all treated as the same in
            #     markdown.
                lst_itms = block.split("\n")
                lst_itms = list(map(lambda itm: itm[2:], lst_itms))
                lst_children = []
                for text in lst_itms:
                    children = text_to_children(text)
                    lst_children.append(ParentNode("li", children))
                block_nodes.append(ParentNode("ul", lst_children))

            case BlockType.CODE:
                code_block = block.removeprefix("```")
                code_block = code_block.removeprefix("\n")
                code_block = code_block.removesuffix("```")
                code_text_node = TextNode(code_block, TextType.CODE)
                child = text_node_to_html_node(code_text_node)
                block_nodes.append(ParentNode("pre", [child]))
            case _:
                raise ValueError(f"Block Type: {block_type} not "
                                 "handled by markdown_to_html_node()")
    return ParentNode("div", block_nodes)

"""
@text: block of markdown text
@return: list of html nodes corresponding to the inline text
"""
def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return children