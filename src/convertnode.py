import re

from htmlnode import LeafNode, ParentNode
from markdownnode import markdown_to_blocks, block_to_block_type, BlockType
from nodesplitter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

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

def text_to_children(block):
    text_nodes = text_to_text_nodes(block)
    # print(f"text_nodes: {text_nodes}")
    html_nodes = []

    for text_node in text_nodes:
        # print(f"text_node: {text_node}")
        node = text_node_to_html_node(text_node)
        # print(type(node))
        # print(f"html_node: {node}")
        html_nodes.append(node)
    
    # print(f"html_nodes: {html_nodes}")
    return html_nodes

def code_block_to_html_node(block):
    content = re.sub(r"^```(\n)?", "", block) # Remove code markdown and first newline if it exists
    content = content.removesuffix("```") # Remove the trailing code markdown
    return ParentNode("pre", [text_node_to_html_node(TextNode(content, TextType.CODE))])

def paragraph_block_to_html_node(block):
    content = block.strip() # Remove leading and trailing whitespace
    content = content.replace("\n", " ") # All new lines should be spaces. HTML renderer should handle where new lines go.
    return ParentNode("p", text_to_children(content))

def heading_block_to_html_node(block):
    heading = re.match(r"(#+ )(.*)", block)
    markdown_count = heading.group(1).count("#")
    content = heading.group(2)
    heading_level = markdown_count if markdown_count <= 6 else 6
    return ParentNode(f"h{heading_level}", text_to_children(content))

def quote_block_to_html_node(block):
    lines = block.split("\n")
    for i in range(0, len(lines)):
        lines[i] = re.sub(r"^> ?", "", lines[i])
    content = "\n".join(lines)
    return ParentNode("blockquote", text_to_children(content))

def ordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        content = re.sub(r"^[\d]\. ", "", line)
        list_items.append(ParentNode("li", text_to_children(content)))
    return ParentNode("ol", list_items)

def unordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        content = re.sub(r"^- ", "", line)
        list_items.append(ParentNode("li", text_to_children(content)))
    return ParentNode("ul", list_items)

def block_to_html_nodes(block):
    block_type = block_to_block_type(block)
    # print(f"block_type: {block_type}")
        
    match block_type:
        case BlockType.CODE:
            return code_block_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_block_to_html_node(block)
        case BlockType.HEADING:
            return heading_block_to_html_node(block)
        case BlockType.QUOTE:
            return quote_block_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_block_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_block_to_html_node(block)
        case _:
            raise ValueError("No matching block type.")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    # print(f"blocks: {blocks}")
    children = []
    for block in blocks:
        children.append(block_to_html_nodes(block))
    html = ParentNode("div", children)
    # print(f"html: {html.to_html()}")
    return html