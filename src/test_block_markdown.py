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
        ul_block    = "- This is a list\n- with items"
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