import unittest
from block_markdown import *

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_type(self):
        self.assertEqual(BlockType.CODE.value,
                         "code")
        self.assertEqual(BlockType.HEADING.value,
                         "heading")
        self.assertEqual(BlockType.OLIST.value,
                         "ordered list")
        self.assertEqual(BlockType.PARAGRAPH.value,
                         "paragraph")
        self.assertEqual(BlockType.QUOTE.value,
                         "quote")
        self.assertEqual(BlockType.ULIST.value,
                         "unordered list")

    def test_block_to_block_type(self):
        # Happy path variables
        head_block1 = "# heading 1"
        head_block2 = "## heading 2"
        head_block3 = "### heading 3"
        head_block4 = "#### heading 4"
        head_block5 = "##### heading 5"
        head_block6 = "###### heading 6"
        code_block  = "```if True:\n    hello world```"
        quot_block1 = ">no space quote"
        quot_block2 = "> space quote"
        ul_block    = "- This is a list\n* with several\n+ items"
        ol_block    = "1. This is an ordered list\n2. with items"

        # Error variables
        head_err1 = "####### heading 7"
        head_err2 = " ###### heading 6"
        code_err  = "```if True:    hello world```"
        quot_err  = " >leading space quote"
        ul_err    = "- This is an accidental list\nof one item"
        ol_err    = "1. This is a bad\nordered list"

        # Happy path checks
        self.assertEqual(block_to_block_type(head_block1),
                         BlockType.HEADING)
        self.assertEqual(block_to_block_type(head_block2),
                         BlockType.HEADING)
        self.assertEqual(block_to_block_type(head_block3),
                         BlockType.HEADING)
        self.assertEqual(block_to_block_type(head_block4),
                         BlockType.HEADING)
        self.assertEqual(block_to_block_type(head_block5),
                         BlockType.HEADING)
        self.assertEqual(block_to_block_type(head_block6),
                         BlockType.HEADING)
        self.assertEqual(block_to_block_type(code_block),
                         BlockType.CODE)
        self.assertEqual(block_to_block_type(quot_block1),
                         BlockType.QUOTE)
        self.assertEqual(block_to_block_type(quot_block2),
                         BlockType.QUOTE)
        self.assertEqual(block_to_block_type(ul_block),
                         BlockType.ULIST)
        self.assertEqual(block_to_block_type(ol_block),
                         BlockType.OLIST)

        # Error checks
        self.assertEqual(block_to_block_type(head_err1),
                         BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(head_err2),
                         BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(code_err),
                         BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(quot_err),
                         BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(ul_err),
                         BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(ol_err),
                         BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag"
            " here</p><p>This is another paragraph with <i>italic"
            "</i> text and <code>code</code> here</p></div>",
    )

    def test_headings(self):
        self.maxDiff = None
        md = """
#      This is a
Heading with   
line
breaks

## This is    another
Heading  with    long strings of spaces

### This is a Heading with an **inline bold statement** 

#### This is a Heading with _inline italics_

##### This is a Heading with `inline code`

###### This is a Heading with an [inline link](wowhead.com) and an
![inline image](img.png)  
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            ("<div><h1>This is a Heading with line breaks</h1><h2>"
             "This is another Heading with long strings of spaces"
             "</h2><h3>This is a Heading with an <b>inline bold "
             "statement</b></h3><h4>This is a Heading with <i>inline"
             " italics</i></h4><h5>This is a Heading with <code>"
             "inline code</code></h5><h6>This is a Heading with an "
             "<a href=\"wowhead.com\">inline link</a> and an "
             "<img src=\"img.png\" alt=\"inline image\"></img></h6>"
             "</div>"),
        )

    def test_blockquote(self):
        md = """
>*First* line of the blockquote
> __Second__ line of the blockquote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            ("<div><blockquote><i>First</i> line of the blockquote "
             "<b>Second</b> line of the blockquote</blockquote></div>"),
        )

    def test_ordered_list(self):
        self.maxDiff = None
        md = """
1. _First_ entry in the list
2. **Second** entry in the list
3. `Third` entry in the list
4. Fourth entry in the list
5. Fifth entry in the list
6. Sixth entry in the list
7. Seventh entry in the list
8. Eighth entry in the list
9. Ninth entry in the list
10. Tenth entry in the list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            ("<div><ol><li><i>First</i> entry in the list</li><li>"
             "<b>Second</b> entry in the list</li><li><code>Third"
             "</code> entry in the list</li><li>Fourth entry in the "
             "list</li><li>Fifth entry in the list</li><li>Sixth "
             "entry in the list</li><li>Seventh entry in the list"
             "</li><li>Eighth entry in the list</li><li>Ninth entry "
             "in the list</li><li>Tenth entry in the list</li></ol>"
             "</div>"),
        )

    def test_unordered_list(self):
        self.maxDiff = None
        md = """
- *First* entry in the list
* __Second__ entry in the list
+ `Third` entry in the list
+ Fourth entry in the list
* Fifth entry in the list
- Sixth entry in the list
- Seventh entry in the list
* Eighth entry in the list
+ Ninth entry in the list
- Tenth entry in the list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            ("<div><ul><li><i>First</i> entry in the list</li><li>"
             "<b>Second</b> entry in the list</li><li><code>Third"
             "</code> entry in the list</li><li>Fourth entry in the "
             "list</li><li>Fifth entry in the list</li><li>Sixth "
             "entry in the list</li><li>Seventh entry in the list"
             "</li><li>Eighth entry in the list</li><li>Ninth entry "
             "in the list</li><li>Tenth entry in the list</li></ul>"
             "</div>"),
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe"
            " **same** even with inline stuff\n</code></pre></div>",
    )

if __name__ == "__main__":
    unittest.main()