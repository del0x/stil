from src.textnode import TextNode, TextType


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