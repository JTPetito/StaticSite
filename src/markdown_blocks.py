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


