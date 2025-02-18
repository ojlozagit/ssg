from textnode import TextType, TextNode


def main():
    node1 = TextNode("This is a text node",
                      TextType.BOLD,
                     "https://www.boot.dev")
    print(node1)


if __name__ == "__main__":
    main()