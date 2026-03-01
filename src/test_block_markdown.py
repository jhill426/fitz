import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph_plain_text(self):
        block = "This is just a regular paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "This is a paragraph.\nWith multiple lines.\nBut no special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h2(self):
        block = "## Heading level 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### Smallest heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_not_heading_no_space(self):
        block = "#no space after hash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_not_heading_too_many_hashes(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_not_heading_only_hashes(self):
        block = "######"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ncode here\nmore code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_empty(self):
        block = "```\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_single_line(self):
        block = "```\nx = 1\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_not_code_no_newline_after_open(self):
        block = "```code without newline```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_not_code_no_close(self):
        block = "```\nunclosed code block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_with_space_after_gt(self):
        block = "> This is a quote with space after >"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_multiline(self):
        block = "> Line one\n> Line two\n> Line three"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_no_space_after_gt(self):
        block = ">No space after >"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_mixed(self):
        block = "> Line one\n>Line two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_not_quote_partial(self):
        block = "> Line one\nNot a quote line"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_single_item(self):
        block = "- First item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple_items(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_not_list_no_space(self):
        block = "-no space after dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_not_list_partial(self):
        block = "- First item\nNot a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_single_item(self):
        block = "1. First item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple_items(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_not_sequential(self):
        block = "1. First\n3. Skipped two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_not_starting_at_one(self):
        block = "2. Started at two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_not_list_no_space(self):
        block = "1.No space after period"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_double_digit(self):
        block = "1. One\n2. Two\n3. Three\n4. Four\n5. Five\n6. Six\n7. Seven\n8. Eight\n9. Nine\n10. Ten"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph_with_inline_markdown(self):
        block = "This has **bold** and _italic_ but is still a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToBlocks(unittest.TestCase):
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
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
