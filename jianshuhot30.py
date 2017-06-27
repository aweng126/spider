import requests
from requests.exceptions import RequestException
import re

def get_one_page(url):
   try:
        responce=requests.get(url)
        if responce.status_code==200:
            return responce.text
        return None
   except RequestException:
       return  None

def parse_one_page(html):
    pattern = re.compile(
        '<li.*?blue-link".*?>(.*?)</a>.*?title".*?href="(.*?)">(.*?)</a>.*?abstract">(.*?)</p>.*?ic-list-read">.*?</i>(.*?)</a>.*?ic-list-comments.*?</i>(.*?)</a>.*?ic-list-like.*?</i>(.*?)</span>.*?ic-list-money.*?</i>(.*?)</span>.*?</li>',
        re.S)
    items=re.findall(pattern,html)
    #print(items)

    for item in items:
        yield {
            'author':item[0],
            'link':item[1],
            'title':item[2],
            'abstract':item[3].strip(),
            'read-num':item[4].strip(),
            'comment-num':item[5].strip(),
            'like-num':item[6],
            'money-num':item[7]
        }

def main():
    url = 'http://www.jianshu.com/trending/monthly?utm_medium=index-banner-s&utm_source=desktop'
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)


if __name__=='__main__':
    main()