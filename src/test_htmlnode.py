import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

TEST_PROPS = [
    ("href", "https://www.google.com"),
    ("target", "_blank")
]
TEST_TAGS = [
    "a",
    "p"
]
TEST_VALUES = [
    "test string",
    ""
]

class TestHTMLNode(unittest.TestCase):

    def test_to_html_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_default_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_empty_dict_props(self):
        test_props = {}
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), "")
    
    def test_one_prop(self):
        test_props = {
            TEST_PROPS[0][0]: TEST_PROPS[0][1]
        }
        test_output = f" {TEST_PROPS[0][0]}=\"{TEST_PROPS[0][1]}\""
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), test_output)

    def test_multiple_props(self):
        test_props = {
            TEST_PROPS[0][0]: TEST_PROPS[0][1],
            TEST_PROPS[1][0]: TEST_PROPS[1][1]
        }
        test_output = f" {TEST_PROPS[0][0]}=\"{TEST_PROPS[0][1]}\" {TEST_PROPS[1][0]}=\"{TEST_PROPS[1][1]}\""
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), test_output)

    def test_prop_with_empty_string(self):
        test_props = {
            TEST_PROPS[0][0]: "",
            TEST_PROPS[1][0]: ""
        }
        test_output = f" {TEST_PROPS[0][0]}=\"\" {TEST_PROPS[1][0]}=\"\""
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), test_output)

class TestLeafNode(unittest.TestCase):
    def test_no_children(self):
        node = LeafNode(TEST_TAGS[0], TEST_VALUES[0])
        self.assertEqual(node.children, None)

    def test_tags(self):
        for tag in TEST_TAGS:
            self.tag_test(tag)

    def tag_test(self, tag):
        node = LeafNode(tag, TEST_VALUES[0])
        self.assertEqual(node.to_html(), f"<{tag}>{TEST_VALUES[0]}</{tag}>")
    
    def test_missing_value_error(self):
        node = LeafNode(TEST_TAGS[0], None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_props(self):
        test_props = {
            TEST_PROPS[0][0]: TEST_PROPS[0][1],
            TEST_PROPS[1][0]: TEST_PROPS[1][1]
        }
        node = LeafNode(TEST_TAGS[0], TEST_VALUES[0], test_props)
        self.assertEqual(node.to_html(), f"<{TEST_TAGS[0]} {TEST_PROPS[0][0]}=\"{TEST_PROPS[0][1]}\" {TEST_PROPS[1][0]}=\"{TEST_PROPS[1][1]}\">{TEST_VALUES[0]}</{TEST_TAGS[0]}>")

class TestParentNode(unittest.TestCase):
    def test_no_children_error(self):
        node = ParentNode(TEST_TAGS[0], None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_no_tag_error(self):
        node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()