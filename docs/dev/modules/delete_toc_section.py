class DeleteTOCSection:
    """
    A class to remove the Table of Contents (ToC) section from a README.md file.
    """

    def __init__(self, filepath):
        """
        Initializes the DeleteTOCSection with a specific README.md file path.
        
        Args:
            filepath (str): Path to the README.md file.
        """
        self.filepath = filepath

    def delete(self):
        """
        Removes the ToC section from the README.md file, including any content
        between "# Table of Contents" and the next section marked by "#".
        """
        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Initialize flags and container for updated content
        in_toc = False
        new_content = []

        for line in lines:
            if line.strip().startswith('# Table of Contents'):
                in_toc = True  # Mark the start of the ToC section
                continue  # Skip adding this line to new content
            if in_toc and line.startswith('#'):
                in_toc = False  # Found the next section, mark end of ToC
            if not in_toc:
                new_content.append(line)  # Add lines outside ToC section

        # Write the modified content back to the README.md
        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.writelines(new_content)
