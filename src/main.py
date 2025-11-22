from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode    

def main():
    print(TextNode("TESTCODE", TextType.ITALIC_TEXT, None))

if __name__ == "__main__":
    main()