import unittest

from textnode import TextNode, TextType
from nodesplitter import split_nodes_delimiter

class TestNodeSplitter(unittest.TestCase):
    def test_code_delimeter(self):
        expected_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes, expected_list)

    def test_italic_delimeter(self):
        expected_list = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, expected_list)

    def test_bold_delimeter(self):
        expected_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, expected_list)
    
    def test_not_text_alone(self):
        expected_list = [
            TextNode("This is an italic text block", TextType.ITALIC),
        ]
        node = TextNode("This is an italic text block", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes, expected_list)

    def test_not_text_multple_nodes(self):
        expected_list = [
            TextNode("This is an italic text block", TextType.ITALIC),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        nodes = [
            TextNode("This is an italic text block", TextType.ITALIC),
            TextNode("This is text with a **bold** word", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertListEqual(new_nodes, expected_list)
    
    def test_multiple_delimeters(self):
        expected_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word, and an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        node = TextNode("This is text with a **bold** word, and an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, expected_list)

    def test_missing_closing_delimeter(self):
        node = TextNode("This is text missing a closing **bold delimeter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delimeter_at_start(self):
        expected_list = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" word is at start", TextType.TEXT),
        ]
        node = TextNode("**Bold** word is at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, expected_list)
    
    def test_delimeter_at_end(self):
        expected_list = [
            TextNode("Italic word is at ", TextType.TEXT),
            TextNode("end", TextType.ITALIC),
        ]
        node = TextNode("Italic word is at _end_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, expected_list)