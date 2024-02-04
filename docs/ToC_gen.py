# Python code to read the README.md file and extract sections marked with #, ##, and ### to create a Table of Contents

def generate_toc(filepath):
    toc = []
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('#'):
                indent_level = line.count('#') - 1
                title = line.strip('#').strip()
                slug = title.lower().replace(' ', '-').replace('/', '').replace('(', '').replace(')', '')
                toc.append(('    ' * indent_level) + f"- [{title}](#{slug})")
    return toc

# Assuming the filepath to the README.md file is correctly specified
filepath = 'README.md'
toc = generate_toc(filepath)

# Joining the list into a multi-line string to form the markdown TOC
toc_md = '\n'.join(toc)
print(toc_md)
