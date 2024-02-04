import difflib

class ReadmeManager:
    """
    A class to manage README.md file operations such as generating a table of contents,
    adding back to table of contents links, removing existing back links, and managing the TOC section.
    """
    
    def __init__(self, filepath='README.md'):
        """
        Initializes the ReadmeManager with a specific README.md file path.
        
        Args:
            filepath (str): Path to the README.md file. Defaults to 'README.md'.
        """
        self.filepath = filepath
        self.back_to_toc_line = "[🔙 Back to Table of Contents](#table-of-contents)\n"

    def generate_toc(self):
        """
        Generates a markdown table of contents for the README.md file based on header tags.
        
        Returns:
            list: A list of markdown links representing the table of contents.
        """
        toc = []
        with open(self.filepath, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('#'):
                    indent_level = line.count('#') - 1
                    title = line.strip('#').strip()
                    slug = title.lower().replace(' ', '-').replace('/', '').replace('(', '').replace(')', '').replace(':', '').replace(',', '').replace('.', '')
                    toc.append(('    ' * indent_level) + f"- [{title}](#{slug})")
        return toc

    def add_back_links(self):
        """
        Adds a 'Back to Table of Contents' link before each heading level 2 and beyond,
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
                    # Add the back to TOC line if it's not the first ## heading
                    if i == 0 or lines[i-1].strip() != self.back_to_toc_line.strip():
                        new_content.append(self.back_to_toc_line)
                else:
                    # Mark that the first ## heading has been seen
                    seen_first_heading = True
            new_content.append(line)

        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.writelines(new_content)


    def remove_back_links(self):
        """
        Removes all existing back to table of contents links from the README.md file.
        """
        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        new_content = [line for line in lines if line.strip() != self.back_to_toc_line.strip()]

        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.writelines(new_content)

    def delete_toc_section(self):
        """
        Correctly identifies and removes the Table of Contents section from the README.md file,
        including any content between "# Table of Contents" and the next section marked by "#".
        """
        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Initialize flags and container for updated content
        in_toc = False
        new_content = []

        for line in lines:
            if line.strip().startswith('# Table of Contents'):
                in_toc = True  # Mark the start of the TOC section
                continue  # Skip adding this line to new content
            if in_toc and line.startswith('#'):
                in_toc = False  # Found the next section, mark end of TOC
            if not in_toc:
                new_content.append(line)  # Add lines outside TOC section

        # Write the modified content back to the README.md
        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.writelines(new_content)


    def add_generated_tocx(self):
        """
        Inserts the generated table of contents immediately after the end of the first section 
        marked by a primary heading ('#') in the README.md file. 
        """
        toc = self.generate_toc()
        toc_content = "# Table of Contents\n" + '\n'.join(toc) + '\n\n'

        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Initialize variables to track the first primary heading and subsequent section
        primary_heading_count = 0
        insert_index = None

        for i, line in enumerate(lines):
            if line.startswith('# '):
                primary_heading_count += 1
                if primary_heading_count == 2:  # Identify the end of the section following the first primary heading
                    insert_index = i
                    break

        if insert_index is not None:
            # Reconstruct the file content with the new TOC placement
            updated_content = lines[:insert_index] + [toc_content] + lines[insert_index:]
            with open(self.filepath, 'w', encoding='utf-8') as file:
                file.writelines(updated_content)

    def compare_files(self, file_path1, file_path2):
        """
        Compares two files line by line and prints the differences.

        Args:
        file_path1 (str): The path to the first file for comparison.
        file_path2 (str): The path to the second file for comparison.

        Returns:
        None: This function prints the differences between the two files.
        """
        # Open and read the files to compare
        with open(file_path1, 'r', encoding='utf-8') as file1, open(file_path2, 'r', encoding='utf-8') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        # Use difflib to get the differences between the two file contents
        diff = difflib.unified_diff(
            file1_lines, file2_lines, 
            fromfile=file_path1, 
            tofile=file_path2, 
            lineterm=''
        )

        # Print the differences
        for line in diff:
            print(line)

# Example of using the ReadmeManager class:
# manager = ReadmeManager('README.md')
# toc = manager.generate_toc()
# print('\n'.join(toc))
# manager.add_back_links()
# manager.remove_back_links()
# manager.delete_toc_section()
# manager.add_generated_toc()
# manager.compare_files('README.md', 'READMEc.md')