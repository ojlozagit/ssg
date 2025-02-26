import unittest
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimeter(self):
        node1 = TextNode(
            "*This* is text with a `code block` **word**",
            TextType.TEXT)
        node4 = TextNode(
            "This is text with a code block word",
            TextType.TEXT)
        err_node = TextNode(
            "This is text with a `code block word",
            TextType.TEXT)
        
        nodes1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        nodes2 = split_nodes_delimiter(nodes1, "**", TextType.BOLD)
        nodes3 = split_nodes_delimiter(nodes2, "*", TextType.ITALIC)
        nodes4 = split_nodes_delimiter([node4], "`", TextType.CODE)

        # Reversing call order used for nodes2 and nodes3
        nodes5 = split_nodes_delimiter(nodes1, "*", TextType.ITALIC)
        nodes6 = split_nodes_delimiter(nodes5, "**", TextType.BOLD)

        self.assertEqual(
            repr(nodes1),
            "[TextNode(*This* is text with a , text, None), "
            "TextNode(code block, code, None), "
            "TextNode( **word**, text, None)]"
        )
        self.assertEqual(
            repr(nodes2),
            "[TextNode(*This* is text with a , text, None), "
            "TextNode(code block, code, None), "
            "TextNode( , text, None), "
            "TextNode(word, bold, None)]"
        )
        self.assertEqual(
            repr(nodes3),
            "[TextNode(This, italic, None), "
            "TextNode( is text with a , text, None), "
            "TextNode(code block, code, None), "
            "TextNode( , text, None), "
            "TextNode(word, bold, None)]"
        )
        self.assertEqual(
            repr(nodes4),
            "[TextNode(This is text with a code block word, text, "
            "None)]"
        )
        self.assertEqual(
            repr(nodes5),
            "[TextNode(This, italic, None), "
            "TextNode( is text with a , text, None), "
            "TextNode(code block, code, None), "
            "TextNode( **word**, text, None)]"
        )
        self.assertEqual(
            repr(nodes6),
            "[TextNode(This, italic, None), "
            "TextNode( is text with a , text, None), "
            "TextNode(code block, code, None), "
            "TextNode( , text, None), "
            "TextNode(word, bold, None)]"
        )
        
        with self.assertRaises(ValueError):
            err_nodes = split_nodes_delimiter([err_node], "`",
                                              TextType.CODE)

    def test_extract_markdown(self):
        img_txt = ("This is text with a ![rick roll]"
                   "(https://i.imgur.com/aKaOqIh.gif) and "
                   "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        lnk_txt = ("This is text with a link [to boot dev]"
                   "(https://www.boot.dev) and "
                   "[to youtube](https://www.youtube.com/@bootdotdev)")

        img_extract = extract_markdown_images(img_txt)
        lnk_extract = extract_markdown_links(lnk_txt)
        err_img_extract = extract_markdown_images(lnk_txt)
        err_lnk_extract = extract_markdown_links(img_txt)

        self.assertEqual(
            img_extract,
            [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
            ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        )
        self.assertEqual(
            lnk_extract,
            [('to boot dev', 'https://www.boot.dev'),
            ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        )

        self.assertEqual(err_img_extract, [])
        self.assertEqual(err_lnk_extract, [])

if __name__ == "__main__":
    unittest.main()