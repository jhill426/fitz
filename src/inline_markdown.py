import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes based on a delimiter to extract inline markdown elements.

    Args:
        old_nodes: List of TextNode objects to process
        delimiter: String delimiter to split on (e.g., "`", "**", "*")
        text_type: TextType to apply to text between delimiters

    Returns:
        List of TextNode objects with inline markdown elements extracted

    Raises:
        ValueError: If a closing delimiter is not found
    """
    new_nodes = []

    for node in old_nodes:
        # Only split TEXT type nodes; pass through other types as-is
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Split the text by the delimiter
        parts = node.text.split(delimiter)

        # If we have an even number of parts, there's an unmatched delimiter
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Unmatched delimiter '{delimiter}' found in text: {node.text}"
            )

        # Process each part
        for i, part in enumerate(parts):
            # Skip empty strings
            if part == "":
                continue

            # Even indices are normal text, odd indices are delimited text
            if i % 2 == 0:
                # Normal text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Delimited text (code, bold, italic, etc.)
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def extract_markdown_images(text):
    """
    Extract markdown images from text.

    Args:
        text: Raw markdown text string

    Returns:
        List of tuples containing (alt_text, url) for each image

    Example:
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        returns [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
    """
    # Pattern matches ![alt text](url)
    pattern = r"!\[([^\]]*)\]\(([^\)]+)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract markdown links from text (excluding images).

    Args:
        text: Raw markdown text string

    Returns:
        List of tuples containing (anchor_text, url) for each link

    Example:
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        returns [("to boot dev", "https://www.boot.dev")]
    """
    # Pattern matches [anchor text](url) but not ![alt text](url)
    pattern = r"(?<!!)\[([^\]]+)\]\(([^\)]+)\)"
    matches = re.findall(pattern, text)
    return matches
