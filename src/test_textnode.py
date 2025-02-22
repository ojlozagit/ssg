import unittest

from textnode import *


'''
This test creates two TextNode objects with the same properties and
asserts that they are equal
'''
class TestTextNode(unittest.TestCase):
    ## Equal Test cases
    def test_eq_noUrl(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("This is a text node", TextType.LINK,
                         "https://bootdev.com")
        node2 = TextNode("This is a text node", TextType.LINK,
                         "https://bootdev.com")
        self.assertEqual(node1, node2)

    ## Not Equal Test cases
    def test_neq_text(self):
        node1 = TextNode("This is text node1", TextType.BOLD)
        node2 = TextNode("This is text node2", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_neq_textType(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_neq_url(self):
        node1 = TextNode("This is a text node", TextType.LINK,
                         "https://bootdev.com")
        node2 = TextNode("This is a text node", TextType.LINK,
                         "https://bootdev.con")
        self.assertNotEqual(node1, node2)

    def test_neq_noUrl(self):
        node1 = TextNode("This is a text node", TextType.LINK,
                         "https://bootdev.com")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_to_html(self):
        raw_txt_node = TextNode("This is raw text",
                                TextType.TEXT)
        bld_txt_node = TextNode("This is emboldened text",
                                TextType.BOLD)
        ita_txt_node = TextNode("This is italicized text",
                                TextType.ITALIC)
        cde_txt_node = TextNode("This is code snippet text",
                                TextType.CODE)
        lnk_txt_node = TextNode("This is a text link",
                                TextType.LINK,
                                "https://www.wowhead.com")
        img_txt_node = TextNode("This is alt text for an image",
                                TextType.IMAGE,
                                "image.png")

        self.assertEqual(
            repr(text_node_to_html_node(raw_txt_node)),
            "LeafNode(<None>This is raw text)"
        )
        self.assertEqual(
            repr(text_node_to_html_node(bld_txt_node)),
            "LeafNode(<b>This is emboldened text)"
        )
        self.assertEqual(
            repr(text_node_to_html_node(ita_txt_node)),
            "LeafNode(<i>This is italicized text)"
        )
        self.assertEqual(
            repr(text_node_to_html_node(cde_txt_node)),
            "LeafNode(<code>This is code snippet text)"
        )
        self.assertEqual(
            repr(text_node_to_html_node(lnk_txt_node)),
            "LeafNode(<a href=\"https://www.wowhead.com\">"
            "This is a text link)"
        )
        self.assertEqual(
            repr(text_node_to_html_node(img_txt_node)),
            "LeafNode(<img src=\"image.png\""
            " alt=\"This is alt text for an image\">)"
        )

if __name__ == "__main__":
    unittest.main()