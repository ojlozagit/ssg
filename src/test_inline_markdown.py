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
                   "(https://www.boot.dev) and [to youtube]"
                   "(https://www.youtube.com/@bootdotdev)")

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

    def test_split_images_and_links(self):
        txt_img_node = TextNode(
            "This is text with an ![image]"
            "(https://i.imgur.com/zjjcJKZ.png) and another "
            "![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        txt_lnk_node = TextNode(
            "This is text with a [link]"
            "(https://www.boot.dev) and another "
            "[second link](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        txt_hyb_node = TextNode(
            "This is text with an ![image]"
            "(https://i.imgur.com/zjjcJKZ.png) and a "
            "[link](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_img_nodes = split_nodes_image([txt_img_node])
        new_lnk_nodes = split_nodes_link([txt_lnk_node])

        hyb_img_nodes = split_nodes_image([txt_hyb_node])
        hyb_lnk_nodes = split_nodes_link([txt_hyb_node])

        self.assertListEqual(
            new_img_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE,
                         "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )
        self.assertListEqual(
            new_lnk_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK,
                         "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

        # Ensuring each node splitter only splits its respective
        # markdown syntax
        self.assertListEqual(
            hyb_img_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://www.youtube.com/@bootdotdev)",
                         TextType.TEXT),
            ],
        )
        self.assertListEqual(
            hyb_lnk_nodes,
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ",
                         TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_text_to_textnodes(self):
        text = (
            "__This__ is **text** with *two* _italicized_ words, a "
            "`code block`, a [link](https://boot.dev), and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
            )
        result = [
            TextNode("This", TextType.BOLD),
            TextNode(" is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("two", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" words, a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(", a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(", and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]

        self.assertListEqual(text_to_textnodes(text), result)

if __name__ == "__main__":
    unittest.main()