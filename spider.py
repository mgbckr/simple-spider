import spider_utils
import lxml.html
import html
import time
import os
import os.path
import uuid

# set start page
start_page = 'http://info.cern.ch/hypertext/WWW/TheProject.html'
out_dir = "out"

# create required folders if they do not exist
if not os.path.exists(out_dir):
  os.makedirs(out_dir + "/pages")

# create page list
page_list = []

# add start page
page_list.append(start_page)
page_pointer = 0

while page_pointer < len(page_list):

  # get the first page which has not been visited yet
  page_url = page_list[page_pointer]
 
  print("\n")
  print("###################################################")
  print("Processing: ", page_url)
  print(page_pointer, "/", len(page_list))
  
  # extract link urls and text
  link_urls, text, error = spider_utils.get_webpage(page_url)

  # print number of links
  print("+", len(link_urls), "(max)")

  print("###################################################")

  # save link and text
  if not error:
    file_id=str(uuid.uuid4())
    with open(out_dir + "/pages/" + file_id + ".html", "wb") as page_file:
      page_file.write(text)

    with open(out_dir + "/page_index.txt", "a") as page_index:
      page_index.write(page_url + "|" + file_id + "\n")
  else:
    print("Error:", error)

  # go through the found links 
  for url in link_urls:

    # check if it does not exist in the page list yet
    if url not in page_list:

      # add the url to the page list
      page_list.append(url)
      
      # print added url
      print("                    ", url)

    # print an error message if the url already existed
    else:
      print("URL already exists: ", url)

  # update page pointer (+1)
  page_pointer = page_pointer + 1

  # sleep a little bit to slow down things
  time.sleep(1.0) # 1 second
