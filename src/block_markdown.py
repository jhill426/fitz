from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    """Determine the type of a markdown block.

    Assumes leading and trailing whitespace have already been stripped.
    """
    lines = block.split("\n")

    # Heading: 1-6 # characters, followed by space, then heading text
    if block.startswith("#"):
        if len(block) > 0:
            i = 0
            while i < len(block) and i < 6 and block[i] == "#":
                i += 1
            if i >= 1 and i <= 6 and len(block) > i and block[i] == " ":
                return BlockType.HEADING

    # Code: starts with ```\n, ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # Quote: every line starts with >
    if lines and all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: every line starts with "N. " where N is 1, 2, 3, ...
    if lines:
        if all(
            line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)
        ):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    """Split a raw Markdown document into block-level strings.

    Blocks are separated by blank lines (double newlines).
    Leading/trailing whitespace is stripped from each block.
    Empty blocks are removed.
    """
    blocks = markdown.split("\n\n")
    stripped = [block.strip() for block in blocks]
    return [block for block in stripped if block]
