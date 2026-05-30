import unittest
from htmlnode import HTMLNODE, LeafNode, ParentNode



class TestHTMLNode(unittest.TestCase):
    def test_noteq(self):
        node = HTMLNODE("p","whatever","kids",None )
        self.assertNotEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    def test_eq(self):
        node = HTMLNODE("a", "Click me", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    def test_ed(self):
        node = HTMLNODE("a", "Click me", {"href": "https://www.google.com", "target": "_blank"})
        self.assertNotEqual(node.props_to_html(), {"href": "https://www.google.com", "target": "_blank"} )
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_prop(self):
        node = LeafNode("p", "Hello, world!", {"href": "https://www.google.com", })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"', )
    def test_leaf_to_html_notage(self):
                node = LeafNode(None, "Hello World")
                self.assertEqual(node.to_html(), "Hello World")
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)
    def test_to_html_with_notag(self):
        child_node = LeafNode(None, "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises( ValueError):
             parent_node.to_html()
    def test_to_html_with_nochild(self):
        child_node = LeafNode("b", None)
        parent_node = ParentNode("span", None)
        with self.assertRaises( ValueError):
             parent_node.to_html()
    def test_to_html_with_generation(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        child1_node = ParentNode("a", [child_node])
        child2_node = ParentNode("p",[child1_node])
        child3_node = ParentNode("i", [child2_node])
        parent_node = ParentNode("div", [child3_node])
        self.assertEqual(parent_node.to_html(),"<div><i><p><a><span><b>grandchild</b></span></a></p></i></div>",)
  
    