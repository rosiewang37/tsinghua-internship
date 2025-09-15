import os
from pathlib import Path

def combine_txt_in_folder(folder_path, output_path, encoding="utf-8"):
    """
    Combines all .txt files in the given folder into one output file.

    Parameters:
        folder_path (str or Path): Folder containing .txt files to combine.
        output_path (str or Path): Path to the combined output .txt file.
        encoding (str): Encoding to use when reading/writing files.
    """
    folder = Path(folder_path)
    txt_files = sorted(folder.glob("*.txt"))  # Sort by filename

    if not txt_files:
        print("No .txt files found in the folder.")
        return

    with open(output_path, 'w', encoding=encoding) as outfile:
        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding=encoding) as infile:
                    contents = infile.read()
                    outfile.write(contents)
                    outfile.write("\n")  # Optional: add newline between files
                print(f"Added: {file_path.name}")
            except Exception as e:
                print(f"Error reading {file_path.name}: {e}")
