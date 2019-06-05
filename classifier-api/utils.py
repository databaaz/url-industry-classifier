import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    if element.strip() == "":
        return False
    return True


def fetch_landing_page(url):
    try:
        response = requests.get(url, timeout=(25,30))
        if response:
            html_page = response.text
            soup = BeautifulSoup(html_page, 'html.parser')
            page_texts = soup.findAll(text=True)
            important_texts = filter(tag_visible, page_texts)
            final_site_content = u".".join(x.strip() for x in important_texts)
            title = soup.title
            if title is not None:
                final_site_content = title.text + " " + final_site_content
            return final_site_content
        else:
            print("Invalid Response")
            return None
    except:
        print("Invalid URL/ Timeout")
        return None
