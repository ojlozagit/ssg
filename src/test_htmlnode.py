import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "node",
                         props={"href": "https://www.google.com",
                                "target": "_blank"})
        self.assertEqual(node.props_to_html(),
                         (" href=\"https://www.google.com\""
                          " target=\"_blank\""))
        self.assertNotEqual(node.props_to_html, "")

    def test_to_html(self):
        node = HTMLNode("p", "node")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("a", "node",
                         props={"href": "https://www.google.com",
                                "target": "_blank"})
        par_node = HTMLNode("p", "parNode", [node])

        self.assertEqual(repr(node),
                         "HTMLnode(<a href=\"https://www.google.com\" target=\"_blank\">"
                         "node --> children: None)")
        self.assertEqual(repr(par_node),
                         "HTMLnode(<p>parNode --> children: "
                         "[HTMLnode(<a href=\"https://www.google.com\" target=\"_blank\">"
                         "node --> children: None)])")
        self.assertNotEqual(repr(node), repr(par_node))

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            node = LeafNode("nval")

        with self.assertRaises(TypeError):
            node = LeafNode(value="No tag")

        with self.assertRaises(TypeError):
            node = LeafNode(props={"Missing args": "Tag and Value"})

    def test_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!",
                         {"href": "https://www.google.com"})
        node3 = LeafNode(None, "This is raw text")
        node4 = LeafNode("noVal", None)

        self.assertEqual(node1.to_html(),
                         "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(),
                         '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(node3.to_html(), "This is raw text")

        self.assertNotEqual(node1.to_html(), node2.to_html)
        self.assertNotEqual(node1.to_html(), node3.to_html)
        self.assertNotEqual(node2.to_html(), node3.to_html())

        # LeafNodes should not be created with self.value set to None
        # For some reason, this is checked in to_html, not __init__
        with self.assertRaises(ValueError):
            node4.to_html()

    def test_repr(self):
        node = LeafNode("a", "node",
                         props={"href": "https://www.google.com",
                                "target": "_blank"})
        par_node = HTMLNode("p", "parNode", [node])

        self.assertEqual(repr(node),
                         "LeafNode(<a href=\"https://www.google.com\" target=\"_blank\">"
                         "node)")
        self.assertEqual(repr(par_node),
                         "HTMLnode(<p>parNode --> children: "
                         "[LeafNode(<a href=\"https://www.google.com\" target=\"_blank\">"
                         "node)])")
        self.assertNotEqual(repr(node), repr(par_node))


class TestParentNode(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError):
            node = ParentNode("nchild")

        with self.assertRaises(TypeError):
            node = ParentNode(children=HTMLNode("p",
                                                "child of parent "
                                                "with no tag"))

        with self.assertRaises(TypeError):
            node = LeafNode(props={"Missing args": "Tag and Child"})

    def test_to_html(self):
        pnode1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        pnode2 = ParentNode("header", [pnode1])

        self.assertEqual(
            pnode1.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
            )
        self.assertEqual(
            pnode2.to_html(),
            "<header><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></header>"
        )
        self.assertNotEqual(repr(pnode1), repr(pnode2))

    def test_repr(self):
        node = LeafNode("a", "node",
                         props={"href": "https://www.google.com",
                                "target": "_blank"})
        par_node = ParentNode("p", [node])

        self.assertEqual(repr(node),
                         "LeafNode(<a href=\"https://www.google.com\" target=\"_blank\">"
                         "node)")
        self.assertEqual(repr(par_node),
                         "ParentNode(<p> --> children: "
                         "[LeafNode(<a href=\"https://www.google.com\" target=\"_blank\">"
                         "node)])")
        self.assertNotEqual(repr(node), repr(par_node))


if __name__ == "__main__":
    unittest.main()