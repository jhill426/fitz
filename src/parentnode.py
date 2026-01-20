from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list[HtmlNode], props: dict[str, str] = None):
        super().__init__(tag, None, props, children)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Tag is required for parent nodes")

        if not self.children:
            raise ValueError("Children are required for parent nodes")

        props_html = self.props_to_html()
        children_html = "".join([child.to_html() for child in self.children])

        if props_html:
            return f"<{self.tag} {props_html}>{children_html}</{self.tag}>"
        return f"<{self.tag}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
