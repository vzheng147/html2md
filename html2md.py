import sys
import csv
import os
import re
import tarfile
import shutil
import json
from datetime import datetime
from bs4 import BeautifulSoup
from webpage import Webpage
import converter

def clean_html(raw_html):
  soup = BeautifulSoup(raw_html, 'html.parser')
  content = soup.find('div', {'class': 'mw-parser-output'})

  if not content:
    print("Error: HTML page with no main article content.", file=sys.stderr)
    return ""

  unwanted_selectors = [
    'table', 'div.navbox', 'div.hatnote', 'style', 'script', 'figure', 'img',
    'span.mw-editsection', 'sup.reference', 'div.reflist','div.printfooter',      
    'div.toc', 'div#toc'               
  ]

  # delete all unwanted tags and their nested structure
  for selector in unwanted_selectors:
    for tag in content.select(selector):
      tag.decompose()
  
  return content

def sanitize_filename(title):
    s = title.lower().replace(' ', '_')
    return re.sub(r'[^a-z0-9_]', '', s) + ".md"

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
    
  # temporary directory for processing compression
  temp_dir = os.path.join(output_directory, "temp_processing")
  if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

  processed_files = []
  url_map = {}

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
    
    # parse and clean, keep only elements we want (BeautifulSoup)
    html = clean_html(raw_html)
    if not html:
      return
    
    # convert to markdown
    markdown_output = converter.convert_soup(html)
    filename = sanitize_filename(page.title)
    output_path = os.path.join(temp_dir, filename)

    with open(output_path, 'w', encoding='utf-8') as md_file:
      md_file.write(markdown_output)
    
    processed_files.append(filename)
    # metadata for diffcheck
    url_map[filename] = {"title": page.title, "url": page.url}

  # archive
  if processed_files:
    # add the json.map file to the temporary directory
    with open(os.path.join(temp_dir, "mapping.json"), "w") as f:
      json.dump(url_map, f)

    # create the archive name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_name = f"{timestamp}.tar.gz"
    archive_path = os.path.join(output_directory, archive_name)

    # adding individual files to the archive 
    with tarfile.open(archive_path, "w:gz") as tar:
      for file_name in processed_files:
        tar.add(os.path.join(temp_dir, file_name), arcname=file_name)
      # Add the mapping file
      tar.add(os.path.join(temp_dir, "mapping.json"), arcname="mapping.json")  
      print(f"Created archive: {archive_path}")

  # cleanup the temporary directory
  if os.path.exists(temp_dir):
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()