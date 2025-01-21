from bs4 import BeautifulSoup

from helpers import extract_text_from_text_by_pattern, get_hash, write_to_html_file, read_from_file, is_existing_file_in_directory, crawl
from voz_helpers import clean_comment_text, get_last_page, pre_process_text, get_regex_patterns

url = "https://voz.vn/t/thread-tong-hop-chia-se-ve-muc-luong-tai-cac-cong-ty-part-2.515355/page-2"
id = get_hash(url)
soup = None

print(id)

if(is_existing_file_in_directory(f"{id}.html")):
    soup = BeautifulSoup(read_from_file(f"{id}.html"), "html.parser")
else:
    soup = crawl(url)    
    if(soup == None):
        raise Exception("Failed to crawl")
    else:
        write_to_html_file(f"{id}.html", soup.prettify())

if(soup != None):

    last_page = get_last_page(soup)

    print(last_page)

    posts = soup.find_all("div", class_="bbWrapper")
    print(len(posts))
    for post in posts:
        # print("-----------------------------")
        comment_text = clean_comment_text(post.get_text())
        comment_text = pre_process_text(comment_text)
        extract_data = extract_text_from_text_by_pattern(comment_text, get_regex_patterns())
        if(len(extract_data) > 0):
            print(extract_data)
        # print(comment_text)