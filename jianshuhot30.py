import json

import requests
from requests.exceptions import RequestException
import re
from multiprocessing import Pool

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
        '<li.*?blue-link".*?>(.*?)</a>.*?title".*?href="(.*?)">(.*?)</a>.*?abstract">(.*?)</p>.*?ic-list-read">.*?'
        +'</i>(.*?)</a>.*?ic-list-comments.*?</i>(.*?)</a>.*?ic-list-like.*?</i>(.*?)</span>.*?ic-list-money.*?</i>(.*?)</span>.*?</li>',
        re.S)
    items=re.findall(pattern,html)

    for item in items:
        yield {
            'author':item[0],
            'link':"http://www.jianshu.com"+item[1],
            'title':item[2],
            'abstract':item[3].strip(),
            'read-num':item[4].strip(),
            'comment-num':item[5].strip(),
            'like-num':item[6],
            'money-num':item[7]
        }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()


def main():
    url = 'http://www.jianshu.com/trending/monthly?utm_medium=index-banner-s&utm_source=desktop'
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__=='__main__':
    main()
