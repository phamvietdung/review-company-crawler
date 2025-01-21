
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

def get_regex_patterns():
    import re
    return [
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


def get_last_page(soup):
    return soup.find("li", class_="pageNav-page").get_text()