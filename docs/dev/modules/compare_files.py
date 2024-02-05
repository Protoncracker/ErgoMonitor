import difflib

class CompareFiles:
    """
    A class to compare two files and print the differences or indicate if they are identical.
    """

    def __init__(self, file_path1, file_path2):
        """
        Initializes the CompareFiles object with paths to two files for comparison.

        Args:
            file_path1 (str): The path to the first file for comparison.
            file_path2 (str): The path to the second file for comparison.
        """
        self.file_path1 = file_path1
        self.file_path2 = file_path2

    def compare(self):
        """
        Compares two files line by line and prints the differences. If no differences are found,
        prints a message indicating that the files are identical.

        The comparison includes the lines that differ between the two files,
        prefixed with markers to indicate differences ('-' for lines in file1 but not in file2,
        '+' for lines in file2 but not in file1).
        """
        # Open and read the files to compare
        with open(self.file_path1, 'r', encoding='utf-8') as file1, open(self.file_path2, 'r', encoding='utf-8') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

        # Use difflib to get the differences between the two file contents
        diff = difflib.unified_diff(
            file1_lines, file2_lines,
            fromfile=self.file_path1,
            tofile=self.file_path2,
            lineterm=''
        )

        # Track if any differences are printed
        differences_found = False
        for line in diff:
            if not differences_found:
                differences_found = True  # Mark that differences have been found
            print(line)

        # If no differences were found, print a message indicating so
        if not differences_found:
            print("No differences found between the files.")
