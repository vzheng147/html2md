#!/usr/bin/env python3
import sys
import os
import tarfile
import json
import difflib
from datetime import datetime, timedelta

# finds the archive file that starts with the target YYYY-MM-DD date
def get_archive_path(output_dir, target_date):
    date = target_date.strftime("%Y-%m-%d")
    if not os.path.exists(output_dir):
        return None
    # list all files matching the date
    archives = [f for f in os.listdir(output_dir) if f.startswith(date) and f.endswith(".tar.gz")]
    if not archives:
        return None
    # sort to get the lastest one and return it
    archives.sort()
    return os.path.join(output_dir, archives[-1])

# reads the archive, returns (content_dictionary, mapping_dictionary)
def extract_archive_data(tar_path):
    content = {}
    mapping = {}

    with tarfile.open(tar_path, "r:gz") as tar:
      map_file = tar.extractfile("mapping.json")
      mapping = json.load(map_file) 
      # read all markdown files
      for member in tar.getmembers():
        if member.isfile() and member.name.endswith(".md"):
          f = tar.extractfile(member)
          content[member.name] = f.read().decode('utf-8')

    return content, mapping

def main():
    if len(sys.argv) != 3:
      print("Usage: ./diffcheck <N> <output_dir>", file=sys.stderr)
      sys.exit(1)

    N = int(sys.argv[1])
    output_dir = sys.argv[2]
    today = datetime.now()
    past_date = today - timedelta(days=N)

    # find archives
    today_archive = get_archive_path(output_dir, today)
    past_archive = get_archive_path(output_dir, past_date)
    # check if either archive does not exist
    if not past_archive and not today_archive:
        print(f"Error: no archive from {N} days ago was found.", file=sys.stderr)
        print("Error: no archives were created today (you can run html2md to create one).", file=sys.stderr)
        sys.exit(0)
    if not past_archive:
        print(f"Error: no archive from {N} days ago was found.", file=sys.stderr)
        sys.exit(0)
    if not today_archive:
        print("Error: no archives were created today (you can run html2md to create one).", file=sys.stderr)
        sys.exit(0)

    # extract Data
    past_content, _ = extract_archive_data(past_archive)
    today_content, today_mapping = extract_archive_data(today_archive)
    modified_pages = []

    for filename, text_today in today_content.items():
      if filename in past_content:
        text_past = past_content[filename]
        matcher = difflib.SequenceMatcher(None, text_past, text_today)
            
        if matcher.ratio() < 1.0:
          meta_data = today_mapping.get(filename, {"title": filename, "url": "Unknown URL"})
          modified_pages.append(meta_data)

    if not modified_pages:
      print(f"No changes in any web page content in the last {N} days.")
    else:
      print(f"The following web pages have been modified in the last {N} days:")
      for page in modified_pages:
        print(f"- {page['title']} ({page['url']})")

if __name__ == "__main__":
    main()