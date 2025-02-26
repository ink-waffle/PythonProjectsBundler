import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

def combine_python_files(directory_path: str, output_file: str = "output/combined_script.txt", formats = [".py"], exclude_dirs: set = {'.venv'}):
    directory_path = Path(directory_path).resolve()
    output_file = Path(output_file)

    if not directory_path.exists():
        print(f"Error: Directory '{directory_path}' does not exist")
        return

    python_files = []
    patterns = [("*" + format) for format in formats]
    paths = [file for pattern in patterns for file in directory_path.rglob(pattern)]
    for path in paths:
        # skip exluded
        if any(excluded in path.parts for excluded in exclude_dirs):
            continue
        
        rel_path = path.relative_to(directory_path)
        python_files.append((rel_path, path))

    if not python_files:
        print("No Python files found in the specified directory (excluding specified directories)")
        return

    python_files.sort(key=lambda x: str(x[0]).lower())

    # create the output file
    with output_file.open('w', encoding='utf-8') as outfile:
        for rel_path, full_path in python_files:
            # write file caption
            outfile.write(f"\n{'=' * 40}\n")
            outfile.write(f"# File: {rel_path}\n")
            outfile.write(f"{'=' * 40}\n\n")

            # write the content of the file
            try:
                with full_path.open('r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    outfile.write('\n')
            except Exception as e:
                outfile.write(f"# Error reading file: {str(e)}\n")

    print(f"\nSuccessfully combined {len(python_files)} files into '{output_file}'")
    print("\nProcessed files:")
    for rel_path, _ in python_files:
        print(f"- {rel_path}")


def main():
    parser = argparse.ArgumentParser(description='Combine multiple Python files into a single file.')
    parser.add_argument('directory', help='Directory containing Python files')
    parser.add_argument('-o', '--output', default='output/combined_script.txt',
                      help='Output filename (default: output/combined_script.txt)')
    parser.add_argument('-f', '--formats', nargs='*', default={'.py'},
                      help='Subdirectories to exclude, space-separated (default: .py)')
    parser.add_argument('-e', '--exclude', nargs='*', default={'.venv'},
                      help='Subdirectories to exclude, space-separated (default: .venv)')

    args = parser.parse_args()
    combine_python_files(args.directory, args.output, args.formats, args.exclude)

if __name__ == "__main__":
    main()