from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode    
import os
import shutil

PUBLIC_PATH = './public'
SOURCE_PATH = './static'

def main():
    copy_source(SOURCE_PATH, PUBLIC_PATH)

def clear_dir(dir):
    shutil.rmtree(dir)
    os.mkdir(dir)
    
def recursive_copy(source, dest):
    current_items = os.listdir(source)
    for item in current_items:
        old_path = os.path.join(source, item)
        new_path = os.path.join(dest, item)
        if os.path.isdir(old_path):
            print(f"Making new dir {new_path}")
            os.mkdir(new_path)
            recursive_copy(old_path, new_path)
        else:
            print(f"Copying {old_path} to {new_path}")
            shutil.copy(old_path, new_path)

def copy_source(source, dest):
    if os.path.exists(dest):
        print(f"Found {dest}, clearing contents...")
        clear_dir(dest)
    recursive_copy(source, dest)

if __name__ == "__main__":
    main()