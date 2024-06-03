from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

def markdown_to_blocks(text):
    b = []
    blocks = text.split("\n\n")
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        b.append(block)
    return b

def block_to_block_type(text):
    lines = text.split("\n")
    if text[0] == "#" and text.strip("#")[0] == " ":
        return block_type_heading
    if len(lines) > 1 and text[:3] == "```" and text[-3:] == "```":
        return block_type_code
    
    isQuote = True
    isUnList = True
    isOrList = True
    for i in range(len(lines)):
        if not lines[i][0] == ">":
            isQuote = False
        if not (lines[i][:2] == "* " or lines[i][:2] == "- "):
            isUnList = False
        if not lines[i][:3] == f"{i+1}. ":
            isOrList = False
        if not (isQuote or isUnList or isOrList):
            break
    if isQuote:
        return block_type_quote
    if isOrList:
        return block_type_olist
    if isUnList:
        return block_type_ulist
    return block_type_paragraph

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level+1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    text = block.strip("` ")
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        line = line[3:]
        children.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ol", children)

def ulist_to_html_node(block):
    children = []
    lines = block.split("\n")
    for line in lines:
        line = line[2:]
        children.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ul", children)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line[0] == ">":
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    text = " ".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)
    
