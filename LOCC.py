import os
import pandas as pd
from collections import defaultdict

# Mapping file extensions to programming languages
EXTENSION_TO_LANGUAGE = {
    '.py': 'Python', '.js': 'JavaScript', '.java': 'Java', '.cpp': 'C++', '.c': 'C',
    '.h': 'C Header', '.hpp': 'C++ Header', '.sh': 'Shell Script', '.rb': 'Ruby',
    '.php': 'PHP', '.html': 'HTML', '.css': 'CSS', '.sql': 'SQL', '.go': 'Go',
    '.ts': 'TypeScript', '.yml': 'YAML', '.yaml': 'YAML', '.json': 'JSON',
    '.xml': 'XML', '.txt': 'Text', '.csv': 'CSV'
}

def count_lines_in_file(file_path):
    """Counts the number of lines in a file, ignoring non-text files."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception as e:
        return 0  # Ignore files that can't be read

def is_code_file(filename):
    """Checks if a file is a text-based code file by extension."""
    binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.mp3', '.ogg', '.wav', '.exe', '.dll', '.bin', '.lock', '.zip', '.tar', '.gz', '.rar', '.7z'}
    ext = os.path.splitext(filename)[1].lower()
    return ext in EXTENSION_TO_LANGUAGE and ext not in binary_extensions

def count_loc_by_extension(directory):
    """Counts lines of code grouped by file extensions in the given directory recursively."""
    loc_count = defaultdict(int)
    file_count = defaultdict(int)
    total_files = 0
    ignored_files = 0
    unique_files = set()
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1].lower()
            total_files += 1
            
            if is_code_file(file):  # Only process known code files
                lines = count_lines_in_file(file_path)
                language = EXTENSION_TO_LANGUAGE.get(extension, 'Unknown')
                loc_count[language] += lines
                file_count[language] += 1
                unique_files.add(file_path)
            else:
                ignored_files += 1
    
    return loc_count, file_count, total_files, ignored_files, len(unique_files)

def main():
    directory = input("Enter the directory path: ")
    loc_data, file_data, total_files, ignored_files, unique_files = count_loc_by_extension(directory)
    
    data = [(language, file_data[language], loc_data[language]) for language in sorted(loc_data, key=loc_data.get, reverse=True)]
    df = pd.DataFrame(data, columns=["Language", "Files", "Lines of Code (LOC)"])
    

    print("---------------------------------------------------")
    print(f"   {total_files} total files.")
    print(f"   {unique_files} unique files.")
    print(f"   {ignored_files} files ignored.\n")
    print("--------------Created by: Susovan Garai------------")

    print("---------------------------------------------------")
    print("  Language           Files     Lines of Code (LOC)")
    print("---------------------------------------------------")
    print(df.to_string(index=False, header=False, col_space=12))
    print("---------------------------------------------------")
    print(f"SUM: {unique_files} files | {df['Lines of Code (LOC)'].sum():,} total lines of code")
    print("---------------------------------------------------")
    
if __name__ == "__main__":
    main()
