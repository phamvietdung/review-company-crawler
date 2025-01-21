from bs4 import BeautifulSoup

from helpers import extract_text_from_text_by_pattern, get_hash, write_to_html_file, read_from_file, is_existing_file_in_directory, crawl

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


def clean_comment_text(text):
    import re
    text = text.replace("\n", ". ")
    text = text.replace("\r", "- ")
    text = text.replace("\t", " ")
    text = re.sub(r'\s{2,}', " ", text)
    return text

def pre_process_text(text):
    text = text.replace(". . . .", "\n")
    text = text.replace("Tên công ty", "\nTên công ty")
    text = text.replace("Lương tháng/năm", "\nLương tháng/năm")
    text = text.replace("Vị trí", "\nVị trí")
    text = text.replace("Thời điểm", "\nThời điểm")
    text = text.replace("Bonus", "\nBonus")
    return text

import re
regex_patterns = [
    {
        "name" : "company_name",
        "regex" : r'Tên\scông\sty:[^\n]*'
    },
    {
        "name" : "salary_gross",
        "regex" : r'Lương\stháng\/năm[^\n]*'
    },
    {
        "name" : "position",
        "regex" : r'Vị\strí:[^\n]*'
    },
    {
        "name" : "year",
        "regex" : r'Thời\tdiểm:[^\n]*'
    },
    {
        "name" : "bonus",
        "regex" : r'Bonus:[^\n]*'
    }
]

if(soup != None):
    posts = soup.find_all("div", class_="bbWrapper")
    print(len(posts))
    for post in posts:
        # print("-----------------------------")
        comment_text = clean_comment_text(post.get_text())
        comment_text = pre_process_text(comment_text)
        extract_data = extract_text_from_text_by_pattern(comment_text, regex_patterns)
        if(len(extract_data) > 0):
            print(extract_data)
        # print(comment_text)