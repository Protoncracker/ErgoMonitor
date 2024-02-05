from argparse import ArgumentParser
from modules.generate_toc import GenerateTOC
from modules.add_back_links import AddBackLinks
from modules.remove_back_links import RemoveBackLinks
from modules.delete_toc_section import DeleteTOCSection
from modules.add_generated_toc import AddGeneratedTOC
from modules.compare_files import CompareFiles

def main():
    parser = ArgumentParser(description='This script manages operations on a README.md file, including generating a ToC, managing back-to-ToC links, and comparing files for differences.')
    parser.add_argument('-g', '--generate-toc', action='store_true', help='Generates a markdown ToC based on header tags found in the README.md. Useful for large READMEs to improve navigation.')
    parser.add_argument('-a', '--add-back-links', nargs='?', const="[🔙 Back to ToC](#table-of-contents)", type=str, metavar='BACK_LINK_TEXT', help='Adds a custom "Back to ToC" link before each heading level 2 and beyond. Defaults to "[🔙 Back to ToC](#table-of-contents)".')
    parser.add_argument('-r', '--remove-back-links', action='store_true', help='Removes all existing "Back to ToC" links from the README.md. Use this to clean up or update links as needed.')
    parser.add_argument('-d', '--delete-toc-section', action='store_true', help='Removes the entire ToC section from the README.md. Useful for regenerating or removing outdated ToC sections.')
    parser.add_argument('-t', '--add-generated-toc', action='store_true', help='Inserts a newly generated ToC immediately after the first section marked by a primary heading in the README.md. Ideal for updating the ToC without manual editing.')
    parser.add_argument('-c', '--compare-files', nargs=2, metavar=('FILE1', 'FILE2'), help='Compares two markdown files line by line and outputs the differences. Useful for identifying changes between document versions.')
    parser.add_argument('-f', '--filepath', type=str, default='README.md', help='Specifies the path to the README.md to be operated on. Defaults to "README.md" in the current directory if not specified.')
    
    args = parser.parse_args()
    
    if args.generate_toc:
        toc_generator = GenerateTOC(args.filepath)
        toc = toc_generator.generate()
        print('\n'.join(toc))
        
    if args.add_back_links is not None:
        back_link_adder = AddBackLinks(args.filepath, args.add_back_links)
        back_link_adder.add()
    
    if args.remove_back_links:
        back_link_remover = RemoveBackLinks(args.filepath, args.add_back_links)
        back_link_remover.remove()

    if args.delete_toc_section:
        toc_section_deleter = DeleteTOCSection(args.filepath)
        toc_section_deleter.delete()

    if args.add_generated_toc:
        toc_adder = AddGeneratedTOC(args.filepath)
        toc_adder.add()

    if args.compare_files:
        file_comparer = CompareFiles(*args.compare_files)
        file_comparer.compare()

if __name__ == "__main__":
    main()
