import urllib.request
import urllib.parse
import lxml.html
import lxml.html.clean
import re
from socket import timeout

def get_webpage(url, clean_text=False):

  # download page

  try:
    connection = urllib.request.urlopen(url, timeout=2)
  except timeout:
    return [], None, "timeout"
  except Exception as e:
    return [], None, "fail" 

  page = connection.read()
  connection.close()

  # parse page
  html = lxml.html.fromstring(page)

  # extract links
  links = html.xpath("//a/@href")

  # complete relative links
  complete_links = [ urllib.parse.urljoin(url, link) for link in links ]

  # get text
  text = page

  if clean_text:

    # initialize cleaner
    cleaner = lxml.html.clean.Cleaner()
    cleaner.javascript = True # This is True because we want to activate the javascript filter
    cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter

    # extract text
    text = cleaner.clean_html(html).text_content()

    # remove special characters
    text = re.sub('[^A-Za-z0-9]+', ' ', text)

  return complete_links, text, None


