class HtmlNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        props: dict[str, str] = None,
        children: list["HtmlNode"] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html is not implemented")

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def __eq__(self, other) -> bool:
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self) -> str:
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
