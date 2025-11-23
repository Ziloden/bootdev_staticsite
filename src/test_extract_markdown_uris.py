import unittest

from extract_markdown_uris import extract_markdown_images, extract_markdown_links

class TestMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), ![rick roll](https://i.imgur.com/aKaOqIh.gif), and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ], matches)
    
    def test_extract_markdown_images_skips_links(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), ![rick roll](https://i.imgur.com/aKaOqIh.gif), and a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ], matches)

class TestMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ], matches)
    
    def test_extract_markdown_links_skips_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), ![rick roll](https://i.imgur.com/aKaOqIh.gif), and a linkt [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ], matches)