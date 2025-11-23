import unittest

from textnode import TextNode, TextType
from nodesplitter import split_nodes_delimiter, split_nodes_image, split_nodes_link

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

class TestImageSplitter(unittest.TestCase):
    def test_split_image(self):
        node = TextNode("![foo](https://www.boot.dev/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("foo", TextType.IMAGE, "https://www.boot.dev/image.png")
            ]
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" with trailing text", TextType.TEXT),
            ],
        )

    def test_split_images_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

class TestLinkSplitter(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and another link [to youtube](https://www.youtube.com/@bootdotdev) with trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another link ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" with trailing text", TextType.TEXT),
            ],
        )
    
    def test_split_links_no_links(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])