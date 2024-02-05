class AddBackLinks:
    """
    A class to add 'Back to ToC' links before a specified heading level in a README.md file,
    with an option to skip adding a back link before the first heading of that level.
    """
    def __init__(self, filepath, back_to_toc_line="[🔙 Back to ToC](#table-of-contents)", level='##', skip_first=True):
        """
        Initializes the AddBackLinks with a specific README.md file path, an optional
        custom back link text, the heading level to add back links to, and an option
        to skip the first heading of that level.

        Args:
            filepath (str): Path to the README.md file.
            back_to_toc_line (str): Custom text for the 'Back to ToC' link. Defaults to
                                    "[🔙 Back to ToC](#table-of-contents)".
            level (str): The heading level to add back links to. Defaults to '##'.
            skip_first (bool): Whether to skip adding a back link before the first heading
                               of the specified level. Defaults to True.
        """
        self.filepath = filepath
        self.back_to_toc_line = back_to_toc_line + "\n"
        self.level = level
        self.skip_first = skip_first

    def add(self):
        """
        Adds a 'Back to ToC' link before the specified heading level, with an option to
        skip the first heading.
        """
        new_content = []
        seen_first_heading = False  # Initially, no heading has been seen

        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            # Check if the line starts with the specified heading level and not with an additional '#'
            if line.startswith(self.level) and not line.startswith(self.level + '#'):
                if not seen_first_heading:
                    if self.skip_first:
                        # If skipping the first, mark it as seen but don't add the back link
                        seen_first_heading = True
                    else:
                        # If not skipping, immediately add the back link before the first heading
                        new_content.append(self.back_to_toc_line)
                        seen_first_heading = True
                else:
                    # For subsequent headings, add the back link
                    new_content.append(self.back_to_toc_line)
            elif not seen_first_heading and self.skip_first:
                # Mark as seen if we are skipping to ensure proper handling for the first heading
                seen_first_heading = True

            new_content.append(line)

        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.writelines(new_content)
