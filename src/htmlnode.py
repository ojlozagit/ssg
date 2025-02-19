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
                f"{self.value}\n\t{repr(self.children)})")
    
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

