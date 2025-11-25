import sys
import csv
import os

def main():
  # arg count check
  if len(sys.argv) != 3:
    print("Usage: ./html2md <csv_file_path> <output_directory>", file=sys.stderr)
    sys.exit(1)

  csv_file_path = sys.argv[1]
  output_directory = sys.argv[2]

  # check the filepath existence
  if not os.path.exists(csv_file_path):
    print(f"Error: '{csv_file_path}' does not exist.", file=sys.stderr)
    sys.exit(1)
  if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print(f"Created directory: {output_directory}")
  
if __name__ == "__main__":
    main()