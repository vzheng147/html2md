import sys
import requests
import urllib.parse
from datetime import datetime

class Webpage:
  def __init__(self, title, url, date_str):
    self.title = title.strip()
    self.url = url.strip()
    self.date_str = date_str.strip()

  def should_download(self):
    target_date = datetime.strptime(self.date_str, "%Y-%m-%d").date()
    today = datetime.now().date()
            
    # download if target_date <= today
    if target_date <= today:
      return True
    else:
      return False
    
  def get_html(self):

    try:
      # web url
      if self.url.startswith("http://") or self.url.startswith("https://"):
        # use timeout in case of failure
        response = requests.get(self.url, timeout=10)
        # check for http errors
        response.raise_for_status()
        return response.text
      # local file
      else:
        parsed = urllib.parse.urlparse(self.url).path
        file_path = urllib.parse.unquote(parsed)
              
        with open(file_path, "r", encoding="utf-8") as f:
          return f.read()

    except requests.exceptions.RequestException as e:
      print(f"Error fetching '{self.title}': {e}", file=sys.stderr)
      return None
    except FileNotFoundError:
      print(f"Error: Local file not found for '{self.title}' ({self.url})", file=sys.stderr)
      return None