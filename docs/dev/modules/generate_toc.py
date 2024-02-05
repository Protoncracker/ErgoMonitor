class GenerateTOC:
    """
    A class to generate a markdown table of contents (ToC) for a README.md file based on header tags.
    """
    def __init__(self, filepath):
        """
        Initializes the GenerateTOC with a specific README.md file path.
        
        Args:
            filepath (str): Path to the README.md file.
        """
        self.filepath = filepath

    def generate(self):
        """
        Generates a markdown ToC for the README.md file based on header tags.
        
        Returns:
            list: A list of markdown links representing the ToC.
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
