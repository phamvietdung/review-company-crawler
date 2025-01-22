import os

data_folder = "data"

def get_path(filename):

    if not os.path.exists(f"{os.path.curdir}/{data_folder}"):
        os.makedirs(f"{os.path.curdir}/{data_folder}")

    return f"{os.path.curdir}/{data_folder}/{filename}"

def write_to_file(filename, data):
    with open(get_path(filename), "w", encoding="utf-8") as f:
        f.write(data)

def read_from_file(filename):
    with open(get_path(filename), "r", encoding="utf-8") as f:
        return f.read()
    
def is_existing_file_in_directory(filename):
    import os
    return os.path.exists(get_path(filename))

def get_hash(string):
    import hashlib
    return hashlib.md5(string.encode()).hexdigest()

def crawl(url):

    import cloudscraper
    from bs4 import BeautifulSoup

    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        print(f"Failed to bypass Cloudflare, status code: {response.status_code}")
        return None
    
def extract_text_by_pattern(soup, pattern):
    import re
    return soup.find_all(text=re.compile(pattern))

def json_serilize_data(data):
    import json
    return json.dumps(data, ensure_ascii=False)

def extract_text_from_text_by_pattern(text_content, patterns):
    import re
    # result = []
    item = {}
    for pattern in patterns:
        
        search_result = re.search(pattern["regex"], text_content)
        if search_result:
            # print(search_result)
            # print(search_result.group(0))
            # result.append({"name" : pattern["name"], "value" : search_result.group(0)})

            splited = clean_output_text(search_result.group(0)).split(":")

            if(len(splited) > 1):
                item[pattern["name"]] = clean_output_text(search_result.group(0)).split(":")[1].strip()

    return item

def normalize_text(text):
    if(text == None):
        return ""
    return text.strip()

def clean_output_text(text):
    import re
    text = re.sub(r'\s{2,}', " ", text)
    text = re.sub(r'(\.\s){2,}', " ", text)
    text = re.sub(r'\.{2,}', ".", text)
    return text

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
    text = text.replace("Lương tháng", "\nLương tháng")
    text = text.replace("Lương năm", "\nLương tháng")
    text = text.replace("Vị trí", "\nVị trí")
    text = text.replace("Thời điểm", "\nThời điểm")
    text = text.replace("Bonus", "\nBonus")
    text = text.replace("Số năm kinh nghiệm", "\nSố năm kinh nghiệm")
    text = text.replace("Other benefit", "\nOther benefit") # Noise data, ignore
    text = text.replace("Benefit", "\nBenefit") # Noise data, ignore

    splited = text.split("Click to expand")

    if(len(splited) > 1):
        text = splited[0]

    return text

def get_regex_patterns():
    import re
    return [
        {
            "name" : "company_name",
            "regex" : r'Tên\scông\sty[^\n]*'
        },
        {
            "name" : "salary_gross",
            "regex" : r'Lương\stháng[^\n]*'
        },
        {
            "name" : "salary_gross",
            "regex" : r'Lương\snăm[^\n]*'
        },
        {
            "name" : "position",
            "regex" : r'Vị\strí[^\n]*'
        },
        {
            "name" : "year",
            "regex" : r'Thời\sđiểm[^\n]*'
        },
        {
            "name" : "bonus",
            "regex" : r'Bonus[^\n]*'
        }
    ]

def get_regex_patterns_2():
    return [
        {
            "name" : "company_name",
            "regex" : r'Tên\scông\sty[^\n]*'
        },
        {
            "name" : "salary_gross",
            "regex" : r'Lương\s:[^\n]*'
        },
        {
            "name" : "position",
            "regex" : r'Vị\strí[^\n]*'
        },
        {
            "name" : "year",
            "regex" : r'Thời\sđiểm[^\n]*'
        },
        {
            "name" : "bonus",
            "regex" : r'Bonus[^\n]*'
        }
    ]

def get_last_page(soup):
    pages = soup.find_all("li", class_="pageNav-page")
    if(len(pages) > 0):
        return int(pages[-1].get_text())
