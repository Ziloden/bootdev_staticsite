import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    HREF_STRING = "href"
    TEST_URL = "https://www.google.com"
    TARGET_STRING = "target"
    TEST_TARGET = "_blank"

    def test_default_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_empty_dict_props(self):
        test_props = {}
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), "")
    
    def test_one_prop(self):
        test_props = {
            self.HREF_STRING: self.TEST_URL
        }
        test_output = f" {self.HREF_STRING}=\"{self.TEST_URL}\""
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), test_output)

    def test_multiple_props(self):
        test_props = {
            self.HREF_STRING: self.TEST_URL,
            self.TARGET_STRING: self.TEST_TARGET
        }
        test_output = f" {self.HREF_STRING}=\"{self.TEST_URL}\" {self.TARGET_STRING}=\"{self.TEST_TARGET}\""
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), test_output)

    def test_prop_with_empty_string(self):
        test_props = {
            self.HREF_STRING: "",
            self.TARGET_STRING: ""
        }
        test_output = f" {self.HREF_STRING}=\"\" {self.TARGET_STRING}=\"\""
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), test_output)


if __name__ == "__main__":
    unittest.main()