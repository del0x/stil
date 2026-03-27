from src.textnode import TextNode, TextType
import re


def markdown_to_blocks(markdown):
    paragraphs = markdown.split("\n\n")
    cleaned = []

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue

        lines = [line.lstrip() for line in p.split('\n')]
        cleaned.append("\n".join(lines))
    return cleaned
    
    


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        i = 0
        buffer = [] # letter buffer, ["T", "E", "S", "T"]
        stack = [] # delimiter buffer, [TextType.ITALIC]

        def flush_buffer():
            if not buffer:
                return
            content = "".join(buffer)
            buffer.clear()

            current_type = stack[-1] if stack else TextType.TEXT
            new_nodes.append(TextNode(content, current_type))

        while i < len(text):
            if text.startswith(delimiter, i):
                flush_buffer()

                if stack and stack[-1] == text_type:
                    stack.pop()
                else:
                    stack.append(text_type)

                i += len(delimiter)
            else:
                buffer.append(text[i])
                i += 1

        flush_buffer()

        if stack:
            raise ValueError("Invalid Markdown: unclosed delimiter")
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue
        
        for label, image_path in images:
            split_token = f"![{label}]({image_path})"
            parts = text.split(split_token, 1)

            if len(parts) != 2:
                raise ValueError("Invalid Markdown: image section is not closed")
            
            before, after = parts
            
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            
            new_nodes.append(TextNode(label, TextType.IMAGE, image_path))

            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue
        
        for label, url in links:
            split_token = f"[{label}]({url})"
            parts = text.split(split_token, 1)

            if len(parts) != 2:
                raise ValueError("Invalid Markdown: link section is not closed")
            
            before, after = parts
            
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            
            new_nodes.append(TextNode(label, TextType.LINK, url))

            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


