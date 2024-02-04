def add_back_to_toc_with_emoji_skip_first(filepath):
    """
    Inserts a link back to the Table of Contents above every secondary (##) and tertiary (###) heading
    in the README.md file, starting from the second ## heading, if it's not already there,
    enhancing navigation with a back emoji.

    Args:
    filepath (str): The path to the README.md file to be modified.

    Returns:
    None: Modifies the file in-place, adding navigational links with emojis where necessary, except before the first ## heading.
    """
    new_content = []  # Initialize a list to hold the modified content
    back_to_toc_line = "[🔙 Back to Table of Contents](#table-of-contents)\n"  # Define the line to be added
    heading_counter = 0  # Counter for ## headings

    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        # Increment counter when a ## heading is found
        if line.startswith('##'):
            heading_counter += 1
            # Skip the first ## heading for the back link
            if heading_counter > 1 and (i == 0 or lines[i-1].strip() != back_to_toc_line.strip()):
                new_content.append(back_to_toc_line)
        elif line.startswith('###') and (i == 0 or lines[i-1].strip() != back_to_toc_line.strip()):
            # Add the back link before ### headings
            new_content.append(back_to_toc_line)
        new_content.append(line)  # Append the original line

    # Write the modified content back to the README.md file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(new_content)

# Specify the actual path to your README.md file
filepath = 'README.md'
add_back_to_toc_with_emoji_skip_first(filepath)
