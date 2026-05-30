from enum import Enum
from splitter import markdown_to_blocks, text_to_textnodes
from htmlnode import HTMLNODE,ParentNode,LeafNode
from textnode import text_node_to_html_node, TextNode,TextType
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "head"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
def text_to_children(text):
        textnodes = text_to_textnodes(text)
        result = []
        for node in textnodes:
             result.append(text_node_to_html_node(node))
        return result
def parse_heading(block):
     parts =  block.split(" ", 1)
     level = len(parts[0])
     text = parts[1]
     return level, text
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
       
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
             block = block.replace("\n", " ")
             block_nodes.append(ParentNode("p", text_to_children(block), None ))
             
        elif block_type == BlockType.HEADING:
            level, text = parse_heading(block)
            tag = f"h{level}"
            block_nodes.append(ParentNode(tag,text_to_children(text), None))
        elif block_type == BlockType.CODE:
            text = block[4:-3]
            raw_text_node = TextNode(text, TextType.PLAIN)
            code_leaf = text_node_to_html_node(raw_text_node)
            code_node = ParentNode("code", [code_leaf])
            pre_node = ParentNode("pre", [code_node])
            block_nodes.append(pre_node)
        elif block_type == BlockType.QUOTE:
            cleaned = []
            lines = block.split("\n")
            for line in lines:
                cleaned.append(line.lstrip(">").strip())
            text = " ".join(cleaned)
            block_nodes.append(ParentNode("blockquote",text_to_children(text), None))
        elif block_type == BlockType.UNORDERED_LIST:
            new_lines = block.split("\n")
            li_nodes = []
            for new_line in new_lines:
                text = new_line[2:]
                children = text_to_children(text)
                li_nodes.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ul", li_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            order_lines = block.split("\n")
            ol_nodes = []
            for order_line in order_lines:
                text = order_line.split(". ", 1)[1]
                child =  text_to_children(text)
                ol_nodes.append(ParentNode("li", child))
            block_nodes.append(ParentNode("ol",ol_nodes))
    return ParentNode("div",  block_nodes)