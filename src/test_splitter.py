import unittest

from splitter import split_nodes_delimiter,split_nodes_image,split_nodes_link,text_to_textnodes,markdown_to_blocks
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic_delimiter(self):
        node = TextNode("An _italic_ word here", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("An ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word here", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_bold_in_one_node(self):
        node = TextNode("**bold one** and **bold two**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("", TextType.PLAIN),
            TextNode("bold one", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("bold two", TextType.BOLD),
            TextNode("", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_no_delimiter_in_text(self):
        node = TextNode("plain old text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("plain old text", TextType.PLAIN)])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("oops `unclosed code", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
class TestSplitNodesUrls(unittest.TestCase):
    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
    def test_split_image_empty_text(self):
        node = TextNode("", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("", TextType.PLAIN)], new_nodes)
    def test_split_image_no_images(self):
        node = TextNode("just some plain text", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("just some plain text", TextType.PLAIN)], new_nodes)
    def test_split_image_just_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)",TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertEqual([TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)

    def test_split_link(self):
        node = TextNode("This is text with an [alt](https://i.imgur.com/zjjcJKZ.png) and another [alt2](https://i.imgur.com/3elNhQu.png)",TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("alt", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode(
                "alt2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )
    def test_split_link_empty_text(self):
        node = TextNode("", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("", TextType.PLAIN)], new_nodes)
    def test_split_link_no_link(self):
        node = TextNode("just some plain text", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("just some plain text", TextType.PLAIN)], new_nodes)
    def test_split_link_just_link(self):
        node = TextNode("[image](https://i.imgur.com/zjjcJKZ.png)",TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertEqual([TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)
class TestMergeText(unittest.TestCase):
    def test_text(self):
       nodes =  text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)")
       self.assertListEqual([
    TextNode("This is ", TextType.PLAIN),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.PLAIN),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.PLAIN),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.PLAIN),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
    TextNode(" and a ", TextType.PLAIN),
    TextNode("link", TextType.LINK, "https://boot.dev"),
], nodes)
class TestMarkdownBlock(unittest.TestCase):
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
    def test_markdown_to_blockII(self):
        md = """
IwonderifIdidn'tspacethis

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
add another


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "IwonderifIdidn'tspacethis",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\nadd another",
                "- This is a list\n- with items",
            ],
        )
if __name__ == "__main__":
    unittest.main()