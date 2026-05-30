import unittest
from blocks import block_to_block_type, BlockType, markdown_to_html_node
from splitter import markdown_to_blocks
class TestMarkdownToHTML(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    def test_paragraph(self):
        md = "This is a simple paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is a simple paragraph.</p></div>",
    )

    def test_paragraph_with_inline(self):
        md = "This has **bold**, _italic_, and `code` in it."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This has <b>bold</b>, <i>italic</i>, and <code>code</code> in it.</p></div>",
        )

    def test_multiple_paragraphs(self):
        md = """First paragraph here.

    Second paragraph here.

    Third one too."""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>First paragraph here.</p><p>Second paragraph here.</p><p>Third one too.</p></div>",
        )

    def test_headings(self):
        md = """# Heading one

    ## Heading two

    ### Heading three with **bold**

    ###### Heading six"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading one</h1><h2>Heading two</h2><h3>Heading three with <b>bold</b></h3><h6>Heading six</h6></div>",
        )

    def test_code_block(self):
        md = """```
def greet():
    print("hello")
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>def greet():\n    print(\"hello\")\n</code></pre></div>",
    )

    def test_code_preserves_markdown(self):
        md = """```
**not bold** and _not italic_
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>**not bold** and _not italic_\n</code></pre></div>",
    )

    def test_quote(self):
        md = """> This is a quote
> that spans
> multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>This is a quote that spans multiple lines</blockquote></div>",
    )

    def test_quote_with_inline(self):
        md = "> Quote with **bold** and _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>Quote with <b>bold</b> and <i>italic</i></blockquote></div>",
    )

    def test_unordered_list(self):
        md = """- first
- second
- third"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>first</li><li>second</li><li>third</li></ul></div>",
    )

    def test_unordered_list_with_inline(self):
        md = """- item with **bold**
- item with _italic_
- item with `code`"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>item with <b>bold</b></li><li>item with <i>italic</i></li><li>item with <code>code</code></li></ul></div>",
    )

    def test_ordered_list(self):
        md = """1. one
2. two
3. three"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>",
    )

