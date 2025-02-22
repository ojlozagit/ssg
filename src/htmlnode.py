class HTMLNode():
    # A Node with:
    # no tag is rendered as raw text
    # no value is assumed to have children
    # no children is assumed to have a value
    # no props won't have any attributes
    def __init__(self, tag=None, value=None, children=None,
                       props=None):
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props
    
    def to_html(self):
        raise NotImplementedError("Virtual HTMLNode method")
    
    def props_to_html(self):
        attribs = ""
        if isinstance(self.props, dict):
            for key, val in self.props.items():
                attribs += f" {key}=\"{val}\""
        return attribs
    
    def __repr__(self):
        return (f"HTMLnode(<{self.tag}{self.props_to_html()}>"
                f"{self.value} --> children: {repr(self.children)})")
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return str(self.value)
        return (f"<{self.tag}{self.props_to_html()}>{self.value}"
                f"</{self.tag}>")

    def __repr__(self):
        return (f"LeafNode(<{self.tag}{self.props_to_html()}>"
                f"{self.value})")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes must have a tag")
        if self.children == None:
            raise ValueError("All parent nodes must have a child")
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html

    def __repr__(self):
        return (f"ParentNode(<{self.tag}{self.props_to_html()}> --> "
                f"children: {repr(self.children)})")