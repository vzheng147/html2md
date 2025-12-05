from bs4 import NavigableString, Tag

def convert_soup(soup):
    return process_element(soup)

def process_element(element):
    markdown = ""
    
    # iterate over children to handle nesting
    for child in element.children:
        if isinstance(child, NavigableString):
            text = child.string
            if text:
                markdown += text
        elif isinstance(child, Tag):
            inner_content = process_element(child)
            
            if child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(child.name[1])
                markdown += f"\n\n{'#' * level} {inner_content.strip()}\n\n"
            
            elif child.name == 'p':
                markdown += f"\n{inner_content.strip()}\n"
            
            elif child.name in ['b', 'strong']:
                markdown += f"**{inner_content}**"
            
            elif child.name in ['i', 'em']:
                markdown += f"__{inner_content}__"
            
            elif child.name == 'a':
                href = child.get('href', '')
                if href:
                    markdown += f"[{inner_content}]({href})"
                else:
                    markdown += inner_content
            
            elif child.name == 'code':
                markdown += f"`{inner_content}`"
                
            elif child.name == 'blockquote':
                quoted = "\n".join([f"> {line}" for line in inner_content.split('\n') if line.strip()])
                markdown += f"\n{quoted}\n"

            elif child.name == 'ul':
                markdown += "\n" + process_list(child, ordered=False) + "\n"
                
            elif child.name == 'ol':
                markdown += "\n" + process_list(child, ordered=True) + "\n"

            elif child.name == 'div':
                markdown += inner_content
            
            else:
                markdown += inner_content

    return markdown

def process_list(list_tag, ordered=False):
    output = ""
    index = 1
    for li in list_tag.find_all('li', recursive=False):
        # recurse for content inside the li
        content = process_element(li).strip()
        if ordered:
            output += f"{index}. {content}\n"
            index += 1
        else:
            output += f"* {content}\n"
    return output