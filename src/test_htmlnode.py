import unittest

from htmlnode import HTMLNode, LeafNode


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
        node1 = HTMLNode("a", "node",
                         props={"href": "https://www.google.com",
                                "target": "_blank"})
        node2 = HTMLNode("a", "node2",
                         props={"href": "https://www.google.com",
                                "target": "_blank"})
        node3 = HTMLNode("a", "node",
                         props={"href": "https://www.google.com",
                                "target": "_blank"})
        par_node1 = HTMLNode("p", "parNode", node1)
        par_node2 = HTMLNode("p", "parNode2", node1)
        par_node3 = HTMLNode("p", "parNode", node3)

        # Testing childless nodes
        self.assertNotEqual(repr(node1), repr(node2))
        self.assertEqual(repr(node1), repr(node3))

        # Testing parent nodes
        self.assertNotEqual(repr(par_node1), repr(par_node2))
        self.assertEqual(repr(par_node1), repr(par_node3))

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
        node4 = LeafNode("noneVal", None)

        self.assertEqual(node1.to_html(),
                         "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(),
                         '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(node3.to_html(), "This is raw text")

        self.assertNotEqual(node1.to_html(), node2.to_html)
        self.assertNotEqual(node1.to_html(), node3.to_html)
        self.assertNotEqual(node2.to_html(), node3.to_html())

        with self.assertRaises(ValueError):
            node4.to_html()


if __name__ == "__main__":
    unittest.main()