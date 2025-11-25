
# convert <h1> -> # 1
def convert_heading(tag, text): 
    level = int(tag[1])
    return f"{'#' * level} {text}\n\n"

def convert_paragraph(text):
    return f"{text.strip()}\n\n"

def convert_bold(text):
    return f"**{text}**"

def convert_italic(text):
    return f"__{text}__"

def convert_code(text):
    return f"`{text}`"

def convert_link(element, text):
    url = element.get('href')
    if not url: # link has no text, treat a <p>
        return text
    return f"[{text}]({url})"


def process_element(element, inner_text):
    tag = element.name

    if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        return convert_heading(tag, inner_text)
    
    elif tag == 'p':
        return convert_paragraph(inner_text)
    
    elif tag in ['b', 'strong']:
        return convert_bold(inner_text)
    
    elif tag in ['i', 'em']:
        return convert_italic(inner_text)
    
    elif tag == 'code':
        return convert_code(inner_text)
    
    elif tag == 'a':
        return convert_link(element, inner_text)