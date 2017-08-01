#目的在于爬取网易云所有歌手的信息
import requests

music_url = 'https://music.163.com/#/discover/artist/cat'

music_headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'_ntes_nnid=d31a72d4ce58133d0eb6e1879e5a7c5a,1494942586705; _ntes_nuid=d31a72d4ce58133d0eb6e1879e5a7c5a; _qddaz=QD.jdnrrw.pbhdar.j3bkmjj6; usertrack=c+5+hVkwBak920RaA8HPAg==; _ga=GA1.2.2088883549.1496319403; UM_distinctid=15cde35fde511d-03de6091b571ab-871133d-100200-15cde35fde669e; P_INFO=m13075313106_1@163.com|1499846813|0|mail163|00&99|shd&1499755195&mail163#shd&370100#10#0#0|130106&1|mail163|13075313106@163.com; __s_=1; JSESSIONID-WYYY=0MKvwjFIXEF2%5CCgC%2BE7Z18KoVBW7eex6ScbZlEguiKn%5CHjVkQexKOIReeIW6pc4QIVV%2F4ydIatzrdVksqp4pvw2Td%2BQoej6lBH4GKN1AbPYA41YADe2Bio5SoacXPlvOm3mo3eXIZ3yd6S%2Fay3Xo5%2FRGEe75x7OwqQtM66X9J7eVJiZS%3A1501602509522; _iuqxldmzr_=32; __utma=94650624.2088883549.1496319403.1501508864.1501600710.4; __utmb=94650624.6.10.1501600710; __utmc=94650624; __utmz=94650624.1501600710.4.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    'Host':'music.163.com',
    'Referer':'https://music.163.com/discover/artist/cat',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
}

def get_content(murl,mheaders):
    content = requests.get(murl,headers=mheaders)
    return content

def deal_content():
    pass

def save_content():
    pass

def main():
    content = get_content(music_url,music_headers)
    print(content.text)

if __name__=='__main__':
    main()