import unittest
from src.markdown_to_html_node import (
    markdown_to_html_node
)


import unittest
from src.markdown_to_html_node import markdown_to_html_node


class TestInlineMarkdown(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_levels(self):
        for i in range(1, 7):
            md = "#" * i + " Heading"
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html, f"<div><h{i}>Heading</h{i}></div>")

    def test_quote_block(self):
        md = "> This is a quote\n> spanning multiple lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote spanning multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- item 1\n- item 2\n- item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item 1</li><li>item 2</li><li>item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_inline_link(self):
        md = "This is a [link](https://example.com) inside text."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a <a href=\"https://example.com\">link</a> inside text.</p></div>",
        )

    def test_inline_image(self):
        md = "Here is an image ![alt](image.png) in a paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Here is an image <img src=\"image.png\" alt=\"alt\"> in a paragraph.</p></div>",
        )

    def test_multiple_paragraphs(self):
        md = "Paragraph one.\n\nParagraph two with **bold**."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Paragraph one.</p><p>Paragraph two with <b>bold</b>.</p></div>",
        )

    def test_mixed_blocks(self):
        md = """
        # Heading

        This is a paragraph with **bold** and _italic_.

        - item 1
        - item 2

        1. first
        2. second

        > Quote line
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<h1>Heading</h1>"
            "<p>This is a paragraph with <b>bold</b> and <i>italic</i>.</p>"
            "<ul><li>item 1</li><li>item 2</li></ul>"
            "<ol><li>first</li><li>second</li></ol>"
            "<blockquote>Quote line</blockquote>"
            "</div>"
        )
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()