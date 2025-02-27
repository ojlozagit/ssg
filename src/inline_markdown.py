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
            case "_":
                tmp_txt = text_node.text
                replacement = "-DBL-UNDERSCORE-MARKER-$$-"

                tmp_txt = tmp_txt.replace("__", replacement)
                split_txt = tmp_txt.split(delimiter)
                return list(map(lambda txt: txt.replace(replacement,
                                                        "__"),
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

# Worker function to be wrapped for url markdown -> TextNode
# Currently defaults to TextNode.LINK
'''
@old_nodes: list of TextNodes
@text_type: the TextType of the new url TextNodes 
@return:    list of new TextNodes comprised of the old types and
            new url types
'''
def split_nodes_url(old_nodes, text_type=TextType.LINK):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        md_tups = (extract_markdown_images(old_node.text)
                   if text_type == TextType.IMAGE
              else extract_markdown_links(old_node.text)) 

        # Create the split text for the TextNodes via a regex obj.
        # Useful for compressing all of the different md_links into
        # one common delimiter.
        # Redundant due to the existnece of extract_markdown()
        '''
        delim_start = "!" if text_type == TextType.IMAGE else "(?<!!)"
        md_pattern = re.compile(delim_start + r"\[([^\[\]]*)\]" +
                                              r"\(([^\(\)]*)\)")
        delimiter = "_MD_DELIMITER_$$_"
        tmp_txt = re.sub(md_pattern, delimiter, old_node.text)
        split_txt = tmp_txt.split(delimiter)
        '''

        # Create the split with the tuples from extract_markdown()
        delim_start = "![" if text_type == TextType.IMAGE else "[" 
        old_text    = old_node.text
        for md in md_tups:
            txt = md[0]
            url = md[1]
            delimiter = f"{delim_start}{txt}]({url})"
            new_split = old_text.split(delimiter, 1)
            # Create the text nodes in same loop
            if new_split[0] != "":
                new_nodes.append(TextNode(new_split[0],
                                          TextType.TEXT))
            new_nodes.append(TextNode(txt, text_type, url))
            old_text = new_split[1]
        if old_text != "":
            new_nodes.append(TextNode(old_text, TextType.TEXT))

    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_url(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_url(old_nodes, TextType.LINK)

def text_to_textnodes(text):
    textnodes = [TextNode(text, TextType.TEXT)]
    textnodes = split_nodes_delimiter(textnodes, "*", TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "__", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = split_nodes_link(textnodes)
    textnodes = split_nodes_image(textnodes)
    return textnodes