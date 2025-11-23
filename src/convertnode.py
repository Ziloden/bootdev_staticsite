from textnode import TextNode, TextType
from htmlnode import LeafNode
from nodesplitter import split_nodes_delimiter, split_nodes_image, split_nodes_link

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError(f"{text_node.text_type} not of type {TextType}")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src":text_node.url,"alt":text_node.text})
        case _:
            raise ValueError(f"{text_node.text_type} not a handled type.")

def text_to_text_nodes(text):
    simple_delimeters = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
    ]
    nodes = [
        TextNode(text, TextType.TEXT)
    ]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    for delimeter, text_type in simple_delimeters:
        nodes = split_nodes_delimiter(nodes, delimeter, text_type)
    
    return nodes

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks = []
    for block in split_markdown:
        if block == "":
            continue
        blocks.append(block.strip())
    return blocks
