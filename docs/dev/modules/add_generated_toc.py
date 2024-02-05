from generate_toc import GenerateTOC

class AddGeneratedTOC:
    """
    Adds a generated Table of Contents (ToC) to a markdown file, positioned before the second
    heading found in the document. This approach is designed to accommodate files with an
    introductory section followed by structured headings.
    
    Attributes:
        filepath (str): The path to the markdown file to be updated.
    """

    def __init__(self, filepath):
        """
        Initializes the AddGeneratedTOC instance with the specified markdown file path.
        
        Args:
            filepath (str): Path to the markdown file where the ToC will be added.
        """
        self.filepath = filepath

    def add(self):
        """
        Generates and inserts a ToC based on the markdown file's headers. The ToC is inserted
        immediately before the second heading found in the file, assuming the first heading
        is used for the document title and the second marks the beginning of the main content.
        """
        # Utilize the GenerateTOC class to generate the ToC
        toc_generator = GenerateTOC(self.filepath)
        toc = toc_generator.generate()
        toc_content = "# Table of Contents\n" + '\n'.join(toc) + '\n\n'

        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Initialize variables to track headings and determine the ToC insertion point
        primary_heading_found = False
        insert_index = None

        for i, line in enumerate(lines):
            if line.startswith('#'):
                if primary_heading_found:  # If the first heading was already found
                    insert_index = i  # Mark the insertion point before the second heading
                    break
                else:
                    primary_heading_found = True  # Mark the first heading as found

        # If only one primary heading is found, append the ToC at the end of the document
        if insert_index is None and primary_heading_found:
            insert_index = len(lines)

        # Insert the ToC into the document
        updated_content = lines[:insert_index] + [toc_content] + lines[insert_index:]
        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.writelines(updated_content)
