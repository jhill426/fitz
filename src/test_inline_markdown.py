import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes,
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


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        """Test splitting text with multiple images"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_single_image(self):
        """Test splitting text with a single image"""
        node = TextNode(
            "This has an ![image](https://example.com/img.png) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This has an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_at_start(self):
        """Test image at the start of text"""
        node = TextNode(
            "![start](https://example.com/start.png) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_at_end(self):
        """Test image at the end of text"""
        node = TextNode(
            "Text before ![end](https://example.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_only(self):
        """Test text that is only an image"""
        node = TextNode(
            "![only](https://example.com/only.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("only", TextType.IMAGE, "https://example.com/only.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_no_images(self):
        """Test text with no images"""
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertListEqual(expected, new_nodes)

    def test_split_non_text_type_passthrough(self):
        """Test that non-TEXT type nodes pass through unchanged"""
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("already bold", TextType.BOLD)]
        self.assertListEqual(expected, new_nodes)

    def test_split_multiple_nodes(self):
        """Test processing multiple nodes"""
        nodes = [
            TextNode("Text with ![img1](https://example.com/1.png)", TextType.TEXT),
            TextNode("already an image", TextType.IMAGE, "https://example.com/2.png"),
            TextNode(
                "More text with ![img2](https://example.com/3.png)", TextType.TEXT
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "https://example.com/1.png"),
            TextNode("already an image", TextType.IMAGE, "https://example.com/2.png"),
            TextNode("More text with ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://example.com/3.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_with_empty_alt(self):
        """Test image with empty alt text"""
        node = TextNode(
            "Image with no alt ![](https://example.com/img.png) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Image with no alt ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        """Test splitting text with multiple links"""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_single_link(self):
        """Test splitting text with a single link"""
        node = TextNode(
            "Click [here](https://example.com) to continue",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://example.com"),
            TextNode(" to continue", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_start(self):
        """Test link at the start of text"""
        node = TextNode(
            "[start](https://example.com) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start", TextType.LINK, "https://example.com"),
            TextNode(" text after", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_end(self):
        """Test link at the end of text"""
        node = TextNode(
            "Text before [end](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_only(self):
        """Test text that is only a link"""
        node = TextNode(
            "[only link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("only link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_no_links(self):
        """Test text with no links"""
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertListEqual(expected, new_nodes)

    def test_split_non_text_type_passthrough(self):
        """Test that non-TEXT type nodes pass through unchanged"""
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("already bold", TextType.BOLD)]
        self.assertListEqual(expected, new_nodes)

    def test_split_multiple_nodes(self):
        """Test processing multiple nodes"""
        nodes = [
            TextNode("Text with [link1](https://example.com/1)", TextType.TEXT),
            TextNode("already a link", TextType.LINK, "https://example.com/2"),
            TextNode("More text with [link2](https://example.com/3)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode("already a link", TextType.LINK, "https://example.com/2"),
            TextNode("More text with ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example.com/3"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_consecutive_links(self):
        """Test consecutive links with no text between"""
        node = TextNode(
            "[first](https://one.com)[second](https://two.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINK, "https://one.com"),
            TextNode("second", TextType.LINK, "https://two.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_ignores_images(self):
        """Test that images are not split by split_nodes_link"""
        node = TextNode(
            "This has an ![image](https://example.com/img.png) but no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode(
                "This has an ![image](https://example.com/img.png) but no links",
                TextType.TEXT,
            )
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_with_complex_url(self):
        """Test link with query parameters and fragments"""
        node = TextNode(
            "Visit [search](https://example.com/search?q=test&lang=en#top) page",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode(
                "search", TextType.LINK, "https://example.com/search?q=test&lang=en#top"
            ),
            TextNode(" page", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_all_types(self):
        """Test converting text with all markdown types"""
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_plain_text(self):
        """Test with plain text (no markdown)"""
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_bold(self):
        """Test with only bold text"""
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_italic(self):
        """Test with only italic text"""
        text = "This is *italic* text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_code(self):
        """Test with only code text"""
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_image(self):
        """Test with only an image"""
        text = "Check out this ![image](https://example.com/img.png) here"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_link(self):
        """Test with only a link"""
        text = "Visit [my site](https://example.com) today"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("my site", TextType.LINK, "https://example.com"),
            TextNode(" today", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_multiple_same_type(self):
        """Test with multiple elements of the same type"""
        text = "**bold1** and **bold2** and **bold3**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold3", TextType.BOLD),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_nested_styles(self):
        """Test bold and italic together (note: markdown doesn't nest them)"""
        text = "This is **bold and *italic* together**"
        nodes = text_to_textnodes(text)
        # Bold is processed first, so the entire content becomes BOLD
        # The * characters inside bold text are not processed as italic
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold and *italic* together", TextType.BOLD),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_image_and_link(self):
        """Test with both image and link"""
        text = "![img](https://example.com/img.png) and [link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_complex_combination(self):
        """Test complex combination of multiple types"""
        text = "Start **bold** then *italic* with `code` ![img](https://img.com/1.png) and [link](https://site.com) end"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://img.com/1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://site.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_consecutive_elements(self):
        """Test consecutive elements of different types"""
        text = "**bold***italic*`code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)


if __name__ == "__main__":
    unittest.main()
