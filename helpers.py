def write_to_file(filename, data):
    f = open("demofile3.txt", "w", "utf-8")
    f.write(data)
    f.close()

def write_to_html_file(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)

def read_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
    
def is_existing_file_in_directory(filename):
    import os
    return os.path.exists(filename)

def get_hash(string):
    import hashlib
    return hashlib.md5(string.encode()).hexdigest()

def crawl(url):

    import cloudscraper
    from bs4 import BeautifulSoup

    # Tạo instance cloudscraper
    scraper = cloudscraper.create_scraper()

    # Gửi request
    response = scraper.get(url)

    # Kiểm tra trạng thái
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        print(f"Failed to bypass Cloudflare, status code: {response.status_code}")
        return None
    
def extract_text_by_pattern(soup, pattern):
    import re
    return soup.find_all(text=re.compile(pattern))

def extract_text_from_text_by_pattern(text_content, patterns):
    import re
    result = []
    for pattern in patterns:
        search_result = re.search(pattern["regex"], text_content)
        if search_result:
            # print(search_result)
            # print(search_result.group(0))
            result.append({"name" : pattern["name"], "value" : search_result.group(0)})
    return result