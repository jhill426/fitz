from htmlnode import HtmlNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from inline_markdown import text_to_textnodes


def text_node_to_html_node(text_node: TextNode) -> HtmlNode:
    """Convert a TextNode to an HTMLNode."""
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        children = text_to_children(text_node.text)
        return ParentNode("a", children, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"alt": text_node.text, "src": text_node.url})
    raise ValueError(f"Unknown text type: {text_node.text_type}")


def text_to_children(text: str) -> list[HtmlNode]:
    """Convert inline markdown text to a list of HTMLNode children."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def _block_to_html_paragraph(block: str) -> HtmlNode:
    text = block.replace("\n", " ")
    return ParentNode("p", text_to_children(text))


def _block_to_html_heading(block: str) -> HtmlNode:
    level = 0
    while level < len(block) and level < 6 and block[level] == "#":
        level += 1
    text = block[level + 1 :].strip()
    return ParentNode(f"h{level}", text_to_children(text))


def _block_to_html_code(block: str) -> HtmlNode:
    content = block[4:-3]
    code_node = LeafNode("code", content)
    return ParentNode("pre", [code_node])


def _block_to_html_quote(block: str) -> HtmlNode:
    lines = [line[1:].lstrip() for line in block.split("\n") if line.startswith(">")]
    text = "\n".join(lines)
    return ParentNode("blockquote", text_to_children(text))


def _block_to_html_unordered_list(block: str) -> HtmlNode:
    items = [line[2:].strip() for line in block.split("\n") if line.startswith("- ")]
    li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ul", li_nodes)


def _block_to_html_ordered_list(block: str) -> HtmlNode:
    items = []
    for line in block.split("\n"):
        if ". " in line:
            _, _, content = line.partition(". ")
            items.append(content.strip())
    li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ol", li_nodes)


def _block_to_html_node(block: str) -> HtmlNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return _block_to_html_paragraph(block)
    if block_type == BlockType.HEADING:
        return _block_to_html_heading(block)
    if block_type == BlockType.CODE:
        return _block_to_html_code(block)
    if block_type == BlockType.QUOTE:
        return _block_to_html_quote(block)
    if block_type == BlockType.UNORDERED_LIST:
        return _block_to_html_unordered_list(block)
    if block_type == BlockType.ORDERED_LIST:
        return _block_to_html_ordered_list(block)
    return _block_to_html_paragraph(block)


def markdown_to_html_node(markdown: str) -> HtmlNode:
    """Convert a full markdown document into a single parent HTMLNode (div)."""
    blocks = markdown_to_blocks(markdown)
    children = [_block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
