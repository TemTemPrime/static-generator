from blocks import markdown_to_html_node
from htmlnode import HTMLNODE
from extractor import extract_title
import os
from pathlib import Path
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file_f:
        markdown_content = file_f.read()
    with open(template_path) as file_t:
        template_content = file_t.read()
    html_node  = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_string)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/',f'src="{basepath}')
    dir_name = os.path.dirname(dest_path)
    os.makedirs(dir_name, exist_ok=True)
    with open(dest_path, "w") as file_d:
        file_d.write(template_content)
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for  file in os.listdir(dir_path_content): 
        content_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(content_path):
            file_path = Path(content_path)
            file_extension = file_path.suffix
            if file_extension == ".md":
                html_dest_path = Path(dest_path).with_suffix(".html")
                generate_page(content_path, template_path, html_dest_path,basepath)
        elif os.path.isdir(content_path):
            generate_pages_recursive(content_path, template_path, dest_path,basepath)
