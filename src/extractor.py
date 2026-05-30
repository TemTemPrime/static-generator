import re 
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches
def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("#") and not line.startswith("##"):
            outlined = line.split("# ")
            h1 = outlined[1]
            return h1.strip()
    raise Exception("no h1 header found")
    