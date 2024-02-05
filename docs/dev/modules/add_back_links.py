class AddBackLinks:
    """
    A class to add 'Back to ToC' links before each heading level 2 and beyond
    in a README.md file.
    """
    def __init__(self, filepath, back_to_toc_line="[🔙 Back to ToC](#table-of-contents)"):
        """
        Initializes the AddBackLinks with a specific README.md file path and an optional
        custom back link text.

        Args:
            filepath (str): Path to the README.md file.
            back_to_toc_line (str): Custom text for the 'Back to ToC' link. Defaults to
                                    "[🔙 Back to ToC](#table-of-contents)".
        """
        self.filepath = filepath
        self.back_to_toc_line = back_to_toc_line + "\n"

    def add(self):
        """
        Adds a 'Back to ToC' link before each heading level 2 and beyond,
        starting after the first occurrence of such a heading.
        """
        new_content = []
        seen_first_heading = False  # Flag to track the first occurrence of a ## heading
        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            # Check if the line is a secondary heading (##) or beyond (###, ####, etc.)
            if line.startswith('##'):
                if seen_first_heading:
                    # Add the back to ToC line if it's not the first ## heading
                    if i == 0 or lines[i-1].strip() != self.back_to_toc_line.strip():
                        new_content.append(self.back_to_toc_line)
                else:
                    # Mark that the first ## heading has been seen
                    seen_first_heading = True
            new_content.append(line)

        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.writelines(new_content)
