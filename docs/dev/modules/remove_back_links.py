class RemoveBackLinks:
    """
    A class to remove all existing "Back to ToC" links from the README.md file.
    """

    def __init__(self, filepath, back_link_text="[🔙 Back to ToC](#table-of-contents)"):
        """
        Initializes the RemoveBackLinks with the README.md file path and the specific back link text to remove.
        
        Args:
            filepath (str): Path to the README.md file.
            back_link_text (str): The specific back link text to look for when removing. Defaults to "[🔙 Back to ToC](#table-of-contents)".
        """
        self.filepath = filepath
        self.back_link_text = back_link_text

    def remove(self):
        """
        Removes all instances of the specified back link text from the README.md file.
        """
        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Filter out lines that match the back_link_text
        new_content = [line for line in lines if line.strip() != self.back_link_text.strip()]

        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.writelines(new_content)
