import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()