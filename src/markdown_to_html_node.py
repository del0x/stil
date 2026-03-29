from src.htmlnode import ParentNode, LeafNode
from src.textnode import text_node_to_html_node
from src.blocktype import block_to_block_type, BlockType
from src.split_delimiter import text_to_textnodes, markdown_to_blocks


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        # PARAGRAPH
        if block_type == BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            children.append(
                ParentNode("p", text_to_children(text))
            )

        # HEADING
        elif block_type == BlockType.HEADING:
            line = block.split("\n")[0]

            level = 0
            for c in line:
                if c == "#":
                    level += 1
                else:
                    break

            text = line[level + 1:]
            children.append(
                ParentNode(f"h{level}", text_to_children(text))
            )

        # CODE (special case)
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            code_text = "\n".join(lines[1:-1]) + "\n"

            code_node = ParentNode(
                "code",
                [LeafNode(None, code_text)]
            )

            children.append(
                ParentNode("pre", [code_node])
            )

        # QUOTE
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            stripped = [line.lstrip(">").lstrip() for line in lines]
            text = " ".join(stripped)

            children.append(
                ParentNode("blockquote", text_to_children(text))
            )

        # UNORDERED LIST
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                text = line[2:]
                items.append(
                    ParentNode("li", text_to_children(text))
                )

            children.append(
                ParentNode("ul", items)
            )

        # ORDERED LIST
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for i, line in enumerate(block.split("\n"), start=1):
                prefix = f"{i}. "
                text = line[len(prefix):]

                items.append(
                    ParentNode("li", text_to_children(text))
                )

            children.append(
                ParentNode("ol", items)
            )

    return ParentNode("div", children)
