import unittest
from src.blocktype import block_to_block_type, BlockType


class TestBlockType(unittest.TestCase):
    def test_heading(self):
        assert block_to_block_type("# Hello") == BlockType.HEADING

    def test_code(self):
        block = "```\nprint('hi')\n```"
        assert block_to_block_type(block) == BlockType.CODE

    def test_quote(self):
        block = "> hello\n> world"
        assert block_to_block_type(block) == BlockType.QUOTE

    def test_unordered(self):
        block = "- a\n- b"
        assert block_to_block_type(block) == BlockType.UNORDERED_LIST

    def test_ordered(self):
        block = "1. a\n2. b"
        assert block_to_block_type(block) == BlockType.ORDERED_LIST

    def test_paragraph(self):
        block = "just text"
        assert block_to_block_type(block) == BlockType.PARAGRAPH