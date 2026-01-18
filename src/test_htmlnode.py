import unittest

from htmlnode import HtmlNode
from textnode import TextNode, TextType


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HtmlNode(
            "div",
            "This is a div node",
            [TextNode("This is a text node", TextType.BOLD)],
        )
        node2 = HtmlNode(
            "div",
            "This is a div node",
            [TextNode("This is a text node", TextType.BOLD)],
        )
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
