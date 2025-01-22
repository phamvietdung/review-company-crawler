from bs4 import BeautifulSoup
import json
import time
from common import extract_text_from_text_by_pattern, get_hash, get_regex_patterns_2, json_serilize_data, normalize_text, write_to_file, read_from_file, is_existing_file_in_directory, crawl, clean_comment_text, get_last_page, pre_process_text, get_regex_patterns
from mysql_connection import get_settings, insert_log, insert_review, set_settings

base_url = "https://voz.vn/t/thread-tong-hop-chia-se-ve-muc-luong-tai-cac-cong-ty-part-2.515355"

def get_page_url(base_url, page_number):
    if(page_number == 1):
        return base_url
    return f"{base_url}/page-{page_number}"

def extract_pipeline(post, patterns):
    comment_text = clean_comment_text(post.get_text())
    comment_text = pre_process_text(comment_text)
    extract_data = extract_text_from_text_by_pattern(comment_text, patterns) 
    if(len(extract_data) > 0):
        # print(extract_data)
        # insert_log(json.dumps(extract_data, ensure_ascii=False), get_hash(json.dumps(extract_data, ensure_ascii=False)))

        company_name = normalize_text(extract_data.get("company_name"))
        salary_gross = normalize_text(extract_data.get("salary_gross"))
        position = normalize_text(extract_data.get("position"))
        year = normalize_text(extract_data.get("year"))
        bonus = normalize_text(extract_data.get("bonus"))
        hash_value = get_hash(f"{company_name}_{salary_gross}_{position}_{year}")

        if(company_name == "" or salary_gross == "" or position == ""):
            # print("Invalid data, skipping")
            return False

        insert_review(company_name, salary_gross, position, year, bonus, hash_value, json_serilize_data(extract_data))
        return True


def process_crawl_page_data(url, is_overwrite = False):

    id = get_hash(url)
    soup = None
    number_of_post = 0

    if(is_existing_file_in_directory(f"{id}.html") and is_overwrite == False):
        soup = BeautifulSoup(read_from_file(f"{id}.html"), "html.parser")
    else:
        soup = crawl(url)    
        if(soup == None):
            raise Exception("Failed to crawl")
        else:
            write_to_file(f"{id}.html", soup.prettify())

    if(soup != None):

        posts = soup.find_all("div", class_="bbWrapper")
        number_of_post = len(posts)
        for post in posts:
            try_extract = extract_pipeline(post, get_regex_patterns())
            if(try_extract == False):
                try_extract = extract_pipeline(post, get_regex_patterns_2())

    print(f"[{id}-{number_of_post}]Processing {url}")


# main process
def process(page, is_overwrite = False):
    start_time = time.time()
    url = get_page_url(base_url, page)
    process_crawl_page_data(url, is_overwrite)
    set_settings("current_page", page)
    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time}")

def get_max_page():
    soup = crawl(base_url)
    last_page = get_last_page(soup)
    return last_page

last_page = 1
last_page_entity = get_settings("current_page")
if(last_page_entity != None):
    last_page = int(last_page_entity[1])
    

print("\nCurrent page: ", last_page)

max_page = get_max_page()    

print("\nMax page: ", max_page)
    
current_page = last_page

while(current_page <= max_page):
    if(current_page == last_page):
        process(current_page, is_overwrite = True)
    else:
        process(current_page)
    current_page += 1
    # time.sleep(1)

                
