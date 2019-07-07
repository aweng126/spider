# coding: utf-8
import os
import re
import urllib
import requests
from bs4 import BeautifulSoup

#项目须知 由于知乎更改了账号登陆问题，比较麻烦，所以直接使用浏览器cookie来进行解决。
# date：2019-7-6
# author：kingwen
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'cookie':'_zap=2bffa91b-1411-4852-b9a2-49b06d6c589c; d_c0="AABqm539dw-PTvkNJzZSx_RW2tdUTydmuvA=|1558530476"; _xsrf=bVwO6LqQPazpzN9hgwdN1M3sDERcJjIZ; tst=r; __utmv=51854390.100-1|2=registration_date=20150817=1^3=entry_date=20150817=1; q_c1=6c2694b208be4eab80c87f7aecfdd7a2|1562221463000|1559541337000; __utma=51854390.1537025950.1560520111.1560520111.1562221465.2; __utmz=51854390.1562221465.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/mo-xuan-57-72/collections; capsion_ticket="2|1:0|10:1562381423|14:capsion_ticket|44:MGU5NmY5ZTY5MWY2NGZiOTliNjlmZTk2NDQ0NWYyY2Y=|957f1f7fff7f9393e5db8763714d5305c493cbdba2aa98f35c585e10a60b7331"; z_c0="2|1:0|10:1562381425|4:z_c0|92:Mi4xckY3OUFRQUFBQUFBQUdxYm5mMTNEeVlBQUFCZ0FsVk5jVm9OWGdDQ2FfMFotM01tb3Rya09OZW5KcWU0WUdjN1FR|ac02f254958abfcbc3d7f16d94992c4cc557a601b3b10ceaeaf8546f4deb2368"; tgw_l7_route=80f350dcd7c650b07bd7b485fcab5bf7'
          }

def getPicUrls(murl,mheaders):
    r = requests.get(murl , headers = mheaders)
    soup = BeautifulSoup(r.text)
    urls=[]
    for i in soup.findAll('img'):
        if i.attrs["src"].startswith("https"):
            #print (i.attrs["src"])
            urls.append(i.attrs["src"])
    print("共有"+str(len(urls))+"张图片")
    return urls

def download_url_picture(img_urls, file_path,file_name):
    try:
        #是否有这个路径
        if not os.path.exists(file_path):
        #创建路径
            os.makedirs(file_path)
        i=0
        for img_url in img_urls:
            #获得图片后缀
            file_suffix = os.path.splitext(img_url)[1]
            #print(file_suffix)
                #拼接图片名（包含路径）
            filename = '{}{}{}{}'.format(file_path,os.sep,file_name+str(i),file_suffix)
            print(filename)
            #下载图片，并保存到文件夹中   
            urllib.request.urlretrieve(img_url,filename=filename)
            i+=1
    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        #urllib.request.urlretrieve(i, filename=filename)
        print('错误 ：', e)




if __name__ == '__main__':

    # 如果是单个问题的话直接更改url和路径即可。
    # base_file_path = '/Users/liqingwen/Desktop/pics'
    # file_name ='沙雕表情包'
    # file_path = os.path.join(base_file_path,file_name)
    # question_url= "https://www.zhihu.com/question/310564833/answer/594714780"
    # murl=getPicUrls(question_url,headers)
    # download_url_picture(murl,file_path,file_name)    



    # 如果有一堆要下载，可以建立一个字典来进行存储
    base_url = 'https://www.zhihu.com'
    base_file_path = '/Users/liqingwen/Desktop/pics'
   
    question_dict={
        # '35931586': '你的日常搭配是什么样子？',
        'question/310564833/answer/644962706':'沙雕表情包',
        'question/310564833/answer/594714780':'万能表情包'
    }

    #question_url= "https://www.zhihu.com/question/310564833/answer/594714780"
    #question_url1= "https://www.zhihu.com/question/310564833/answer/594714780"
    #murl=getPicUrls(question_url1,headers)
    #download_url_picture(murl,file_path,file_name)    

    for key in question_dict.keys():
        question_url = os.path.join(base_url,key)
        file_path = os.path.join(base_file_path,question_dict[key])
        #print(file_path)
        #print(key,question_dict[key],key) 
        murl=getPicUrls(question_url,headers)
        download_url_picture(murl,file_path,question_dict[key])      
       # print('下一个答案')

