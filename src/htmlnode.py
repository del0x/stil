class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        result = "".join([f' {key}="{value}"' for key, value in self.props.items()])
        return result if self.props else ""
        
        
    def  __repr__(self):
        return(f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})")
        