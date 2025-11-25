import sys
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