from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode    
from markdownnode import extract_title
from convertnode import markdown_to_html_node

import os
import shutil

PUBLIC_PATH = './public'
STATIC_CONTENT_PATH = './static'

def main():
    copy_source(STATIC_CONTENT_PATH, PUBLIC_PATH)
    generate_pages_recursive('content', 'template.html', 'public')

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

def generate_page(from_path, template_path, dest_path):
    content = ""
    html_content = ""
    template = ""
    updated_template = ""

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as f:
        content = f.read()
        f.close()
    with open(template_path) as f:
        template = f.read()
        f.close()
    
    html_nodes = markdown_to_html_node(content)
    html_content = html_nodes.to_html()
    title = extract_title(content)
    
    updated_template = template.replace('{{ Title }}', title)
    updated_template = updated_template.replace('{{ Content }}', html_content)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, 'w') as f:
        f.write(updated_template)
        f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    current_items = os.listdir(dir_path_content)
    for item in current_items:
        source_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)
        dest_item_basename, dest_item_ext = os.path.splitext(dest_item_path)
        print(dest_item_basename)
        print(dest_item_ext)
        if os.path.isdir(source_item_path):
            generate_pages_recursive(source_item_path, template_path, dest_item_path)
        elif dest_item_ext == ".md":
            generate_page(source_item_path, template_path, f"{dest_item_basename}.html")

    
if __name__ == "__main__":
    main()