class HTMLNODE:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        
    def props_to_html(self):
       if self.props == None:
           return ""
       formatted = ""
       for key in self.props:
           formatted += f' {key}="{self.props[key]}"'
       return formatted
    def __repr__(self):
        return f"HTMLNODE{self.tag}, {self.value}, {self.children}, {self.props}"
class LeafNode(HTMLNODE):
    def  __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def __repr__(self):
        return f"LeafNode{self.tag}, {self.value}, {self.props}"
class ParentNode(HTMLNODE):
    def __init__(self, tag,  children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children is None:
            raise ValueError("MISSING CHILD MISSING CHILD")
        else:
            results = ""
            for child in self.children:
                 results += child.to_html()
                 
        return f"<{self.tag}>{results}</{self.tag}>"