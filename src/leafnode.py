from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Value is required for leaf nodes")

        if not self.tag:
            return self.value

        props_html = self.props_to_html()
        if props_html:
            return f"<{self.tag} {props_html}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
