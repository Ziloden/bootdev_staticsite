import unittest

from markdownnode import markdown_to_blocks, BlockType, block_to_block_type

class TestConvertMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_removes_empty_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line








- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_cleans_up_whitespace(self):
        md = """
This is **bolded** paragraph with trailing whitespace          

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph with trailing whitespace",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
class TestBlockToBlockType(unittest.TestCase):
    # Heading Block Tests

    def test_heading_one(self):
        block = "# Foo"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_six(self):
        block = "###### Foo"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_heading_seven_fails(self):
        block = "####### Foo"
        block_type = block_to_block_type(block)
        # self.assertEqual(block_type, BlockType.HEADING)
        pass

    # Code Block Tests

    def test_code_single_line(self):
        block = "```\nI am a code block\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_code_multi_line(self):
        block = "```\nI am a multiline\ncode block\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_code_is_paragraph_no_closing_backticks(self):
        block = "```\nI am a code block"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_code_is_paragraph_closing_backticks_not_last(self):
        block = "```\nI am a code block\n```Foo"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code_is_paragraph_closing_backticks_not_on_new_line(self):
        block = "```\nI am a code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code_is_paragraph_opening_backticks_not_followed_by_new_line(self):
        block = "```I am a code block\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    # Quote Block Tests

    def test_quote_block_single_line(self):
        block = ">I am a single line quote block"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_block_multiline(self):
        block = ">I am a multiline\n>quote\n>block"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_block_is_paragraph_line_missing_angle_bracket(self):
        block = ">I am a multiline\n>quote\nblock"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    # Unordered List Block Tests

    def test_unordered_list_block_single_line(self):
        block = "- I am an unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unordered_list_block_multiline(self):
        block = "- I am\n- an unordered\n- list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_unordered_list_block_is_paragraph_line_missing_hyphen(self):
        block = "- I am\n- an unordered\n list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

# Ordered List Block Tests

    def test_ordered_list_block_single_line(self):
        block = "1. I am an ordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_block_multiline(self):
        block = "1. I am\n2. an ordered\n3. list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_ordered_list_block_is_paragraph_line_missing_number(self):
        block = "1. I am\n2. an ordered\n list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_block_is_paragraph_line_missing_period(self):
        block = "1. I am\n2. an ordered\n3, list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_block_is_paragraph_line_out_of_order(self):
        block = "1. I am\n2. an ordered\n4. list"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)