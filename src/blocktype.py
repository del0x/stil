from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "undordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    # --- CODE BLOCK ---
    if (
        block.startswith("```") and
        block.endswith("```") and
        len(lines) >= 2
    ):
        return BlockType.CODE

    # --- HEADING ---
    if lines[0].startswith("#"):
        count = 0
        for c in lines[0]:
            if c == "#":
                count += 1
            else:
                break

        if 1 <= count <= 6 and len(lines[0]) > count and lines[0][count] == " ":
            return BlockType.HEADING

    # --- QUOTE ---
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # --- UNORDERED LIST ---
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # --- ORDERED LIST ---
    is_ordered = True
    expected = 1

    for line in lines:
        prefix = f"{expected}. "
        if not line.startswith(prefix):
            is_ordered = False
            break
        expected += 1

    if is_ordered:
        return BlockType.ORDERED_LIST

    # --- DEFAULT ---
    return BlockType.PARAGRAPH