from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "para"
    HEADING = "head"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "ulist"
    ORDERED_LIST = "olist"

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    blocks = []
    for block in split_markdown:
        if block == "":
            continue
        blocks.append(block.strip())
    return blocks

def block_to_block_type(block):
    match_types = {
        r"#{1,6}\s{1}.+": BlockType.HEADING,
        r"```\n[\w\d\s\n]*\n```$": BlockType.CODE,
        r"(>[\w\d\t ]*){1}(\n>[^\n]*)*": BlockType.QUOTE,
        r"(- {1}[\w\d\t ]*){1}(\n- {1}[^\n]*)*": BlockType.UNORDERED_LIST,
    }

    for regex, block_type in match_types.items():
        if re.fullmatch(regex, block):
            return block_type
    return BlockType.PARAGRAPH