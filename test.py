md = """
            This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items
            """

test = md.split("\n\n")


uno = [x.strip(' ') for x in test]

print(uno)