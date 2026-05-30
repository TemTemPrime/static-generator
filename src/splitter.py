from textnode import TextNode,TextType
from extractor import extract_markdown_images, extract_markdown_links
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
        else:
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception(f"{delimiter} is not complete")
            for i in range(len(parts)):

                part = parts[i]
                
                if i % 2 == 0:
                    even_node = TextNode(part, TextType.PLAIN)
                    new_nodes.append(even_node)
                else:
                    odd_node = TextNode(part, text_type)
                    new_nodes.append(odd_node)


    return new_nodes
def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        
        if old_node.text_type != TextType.PLAIN:
             new_nodes.append(old_node)
        else:
            delimiters = extract_markdown_images(old_node.text)
            remaining_text = old_node.text
            if len(delimiters) == 0:
                    new_nodes.append(old_node)
                    continue
            for alt, url in delimiters:
                parts =   remaining_text.split(f"![{alt}]({url})", 1)
                if parts[0] != "":
                    before_image = TextNode(parts[0], TextType.PLAIN)
                    new_nodes.append(before_image)
                image =  TextNode(alt, TextType.IMAGE, url ) 
                new_nodes.append(image)
                remaining_text = parts[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    return new_nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        
        if old_node.text_type != TextType.PLAIN:
             new_nodes.append(old_node)
        else:
            delimiters = extract_markdown_links(old_node.text)
            remaining_text = old_node.text
            if len(delimiters) == 0:
                    new_nodes.append(old_node)
                    continue
            for alt, url in delimiters:
                parts =   remaining_text.split(f"[{alt}]({url})", 1)
                if parts[0] != "":
                    before_link = TextNode(parts[0], TextType.PLAIN)
                    new_nodes.append(before_link)
                link =  TextNode(alt, TextType.LINK, url ) 
                new_nodes.append(link)
                remaining_text = parts[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
    return new_nodes
def text_to_textnodes(text):

    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_",TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes 
def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        result.append(block)
    return result
    