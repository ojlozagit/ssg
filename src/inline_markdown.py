from textnode import TextNode, TextType
import re

'''
 @old_nodes: list of TextNodes
 @delimiter: string consisting of the characters used to split the
             nodes (either markup bold, italic or inline code)
 @text_type: the TextType of the new TextNodes that the delimiter
             creates
 @return:    list of new TextNodes comprised of the old types and
             new types
'''
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # String splitter helper function
    def split_node_text(text_node, delimiter):
        match delimiter:
            case "*":
                # Possible better replacements with more uniqueness
                # 1. Add a random UUID
                # 2. Add special unicode characters
                # 3. Add a timestamp
                tmp_txt = text_node.text
                replacement = "_DBL_ASTERISK_MARKER_$$_"

                tmp_txt = tmp_txt.replace("**", replacement)
                split_txt = tmp_txt.split(delimiter)
                return list(map(lambda txt: txt.replace(replacement,
                                                        "**"),
                                split_txt))
            case _:
                return text_node.text.split(delimiter)
    
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_txt = split_node_text(old_node, delimiter)
        if not (len(split_txt) & 1): # if the length is even
            raise ValueError(f"{repr(old_node)} is missing"
                             f"matching delimeter: {delimiter}")

        is_txt_node = True
        for txt in split_txt:
            if txt == "":
                is_txt_node = not is_txt_node 
                continue

            if is_txt_node:
                new_nodes.append(TextNode(txt, TextType.TEXT))
            else:
                new_nodes.append(TextNode(txt, text_type))
            is_txt_node = not is_txt_node

    return new_nodes

'''
@text: raw markdown text
@return: a list of tuples (alt_text, url) of any markdown images
'''
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


'''
@text: raw markdown text
@return: a list of tuples (anchor_text, url) of any markdown links
'''
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)