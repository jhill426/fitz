import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_single(self):
        """Test splitting a single code block"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_code_multiple(self):
        """Test splitting multiple code blocks in one string"""
        node = TextNode("Text with `code1` and `code2` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" blocks", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold(self):
        """Test splitting bold text with ** delimiter"""
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic(self):
        """Test splitting italic text with * delimiter"""
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_at_start(self):
        """Test when delimiter is at the start of the string"""
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_at_end(self):
        """Test when delimiter is at the end of the string"""
        node = TextNode("Text ends with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_entire_string(self):
        """Test when entire string is delimited"""
        node = TextNode("`entire code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("entire code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        """Test when no delimiter is present"""
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Just plain text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_type_passthrough(self):
        """Test that non-TEXT type nodes pass through unchanged"""
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes_mixed(self):
        """Test processing multiple nodes, some TEXT and some not"""
        nodes = [
            TextNode("Text with `code`", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("More `code` here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("already bold", TextType.BOLD),
            TextNode("More ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter_raises_error(self):
        """Test that unmatched delimiter raises ValueError"""
        node = TextNode("Text with `unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("Unmatched delimiter", str(context.exception))

    def test_empty_delimited_section(self):
        """Test when there's empty text between delimiters"""
        node = TextNode("Text with `` empty", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode(" empty", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_consecutive_delimited_sections(self):
        """Test consecutive delimited sections with no text between"""
        node = TextNode("`code1``code2`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code1", TextType.CODE),
            TextNode("code2", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        """Test extracting a single markdown image"""
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        """Test extracting multiple markdown images"""
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(expected, matches)

    def test_extract_no_images(self):
        """Test text with no images"""
        matches = extract_markdown_images("This is just plain text")
        self.assertListEqual([], matches)

    def test_extract_image_with_empty_alt(self):
        """Test image with empty alt text"""
        matches = extract_markdown_images(
            "Image with no alt ![](https://example.com/img.png)"
        )
        self.assertListEqual([("", "https://example.com/img.png")], matches)

    def test_extract_image_ignores_links(self):
        """Test that regular links are not matched"""
        matches = extract_markdown_images(
            "This has a [link](https://example.com) but no images"
        )
        self.assertListEqual([], matches)

    def test_extract_image_with_complex_url(self):
        """Test image with query parameters and fragments"""
        text = "![logo](https://example.com/logo.png?size=large&v=2#top)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("logo", "https://example.com/logo.png?size=large&v=2#top")], matches
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        """Test extracting a single markdown link"""
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_multiple_links(self):
        """Test extracting multiple markdown links"""
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, matches)

    def test_extract_no_links(self):
        """Test text with no links"""
        matches = extract_markdown_links("This is just plain text")
        self.assertListEqual([], matches)

    def test_extract_links_ignores_images(self):
        """Test that images are not matched as links"""
        matches = extract_markdown_links(
            "This has an ![image](https://example.com/img.png) but no links"
        )
        self.assertListEqual([], matches)

    def test_extract_links_and_images_separate(self):
        """Test that links and images can be distinguished"""
        text = "Link [here](https://example.com) and image ![pic](https://example.com/pic.png)"
        link_matches = extract_markdown_links(text)
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("here", "https://example.com")], link_matches)
        self.assertListEqual([("pic", "https://example.com/pic.png")], image_matches)

    def test_extract_link_with_complex_url(self):
        """Test link with query parameters"""
        text = "[search](https://example.com/search?q=test&lang=en)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("search", "https://example.com/search?q=test&lang=en")], matches
        )

    def test_extract_consecutive_links(self):
        """Test multiple consecutive links"""
        text = "[first](https://one.com)[second](https://two.com)[third](https://three.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("first", "https://one.com"),
            ("second", "https://two.com"),
            ("third", "https://three.com"),
        ]
        self.assertListEqual(expected, matches)


if __name__ == "__main__":
    unittest.main()
