from textnode import TextNode, TextType


def main():
    text_node = TextNode("Hello", TextType.TEXT, "https://www.justinhill.xyz")
    print(text_node)


if __name__ == "__main__":
    main()
