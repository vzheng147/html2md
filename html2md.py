import sys
import csv
import os
from bs4 import BeautifulSoup
from webpage import Webpage
import converter

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
  
  webpages_arr = []
  # reading the csv
  with open(csv_file_path, 'r', encoding='utf-8') as f:
    headers = ['title', 'url', 'date']
    reader = csv.DictReader(f, delimiter='|', fieldnames=headers)

    for line in reader:
      webpage = Webpage(line['title'], line['url'], line['date'])
      webpages_arr.append(webpage)
    
  
  for page in webpages_arr:
    # check the date scheduled <= today's date
    if not page.should_download():
      print(f"[Skipping] {page.title} (Scheduled for Future Date)")
      continue

    print(f"[Processing] {page.title}")
    # download raw HTML
    raw_html = page.get_html()
    if not raw_html:
      print("Failed to download HTML.")
      continue

    





if __name__ == "__main__":
    main()