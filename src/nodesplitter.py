from textnode import TextNode, TextType
from extract_markdown_uris import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # If the wrapping node is not of TextType.TEXT just append it as is.
        # We're not processing nested nodes.
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # If the delimeter count is odd then we have a delimeter with no
        # matching delimeter closing it.
        if old_node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Missing closing delimiter: {old_node.text}")

        split_nodes = []
        split_string = old_node.text.split(delimiter)
        for i in range(0, len(split_string)):
            new_string = split_string[i]

            # Only process the string if it isn't empty; this way we drop
            # the empty bits when the delimeter is either at the beginning
            # or end
            if new_string == "":
                continue
            # If the index is index is odd we're outside the delimeter,
            # if even then inside. When delimeter is at beginning of
            # the string we get an empty string at index 0 so this
            # still works as intended.
            if i % 2 == 0:
                split_nodes.append(TextNode(new_string, TextType.TEXT))
            else:
                split_nodes.append(TextNode(new_string, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # If the wrapping node is not of TextType.TEXT just append it as is.
        # We're not processing nested nodes.
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for alttext, url in extract_markdown_images(old_node.text):
            preceding_text, remaining_text = remaining_text.split(f"![{alttext}]({url})", 1)
            if preceding_text != "":
                new_nodes.append(TextNode(preceding_text, TextType.TEXT))
            new_nodes.append(TextNode(alttext, TextType.IMAGE, url))
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # If the wrapping node is not of TextType.TEXT just append it as is.
        # We're not processing nested nodes.
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        remaining_text = old_node.text
        for text, url in extract_markdown_links(old_node.text):
            preceding_text, remaining_text = remaining_text.split(f"[{text}]({url})", 1)
            if preceding_text != "":
                new_nodes.append(TextNode(preceding_text, TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes