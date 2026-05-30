from extractor import extract_markdown_images, extract_markdown_links, extract_title
import unittest

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an [alttext](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("alttext", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_title(self):
        md = """# Heading one

    ## Heading two

    ### Heading three with **bold**

    ###### Heading six"""
        head = extract_title(md)
        self.assertEqual("Heading one", head)
    def test_extract_edgecase(self):
        md = """#   Hello   
        """
        head = extract_title(md)
        self.assertEqual("Hello", head)
    def test_extract_expect(self):
        md = """  Hello   
        """
        
        with self.assertRaises(Exception):
              extract_title(md)
    