# coding=utf-8
import os
import requests
import json
from bs4 import BeautifulSoup

'''
目标：下载某一微博下面的热门评论，比如榜姐https://m.weibo.cn/detail/4391165086117795
目前实现效果：实现第一轮查询大概18条，之后的url拼凑完成，
            但是第二轮往后查询responce的结果是0，
            应该还有一个预防措施是用来反扒的，在请求头有特殊标志或者是有中间请求结果来确认下一轮的结果。
            但是暂时还没有发现。
时间：20197-7
作者：李庆文
'''
bangjie_url = 'https://m.weibo.cn/comments/hotflow?id=4391165086117795&mid=4391165086117795&max_id_type=0'
base_url_first="https://m.weibo.cn/comments/hotflow?id={0}&mid={0}"
base_url_others= "https://m.weibo.cn/comments/hotflow?id={0}&mid={0}&max_id={1}&max_id_type={2}"

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
          'cookie':'SUB=_2A25x46U5DeRhGeNP6VUV-CfMzTiIHXVTL8txrDV6PUJbkdAKLXftkW1NSdPES4nG3vt3uNbDug-MtbspH73e1wuJ; SUHB=0HThJYoSSfZeVt; SCF=Aklmj_514Pf9qmiPUdZ2-KFWl4jOZSDh2BjDKxAqWUTL5bLo1nVEkU9aOvO3Eoqj-l6bAJDc692v8KGtRE4rzCo.; _T_WM=52575181683; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=c771a2; M_WEIBOCN_PARAMS=oid%3D4391165086117795%26luicode%3D20000061%26lfid%3D4391165086117795%26uicode%3D20000061%26fid%3D4391165086117795',
          'X-XSRF-TOKEN': 'cc524f'
          }

first = True
class Comment:
    def __init__(self,user,content,liked_number,reply_number):
        self.user = user
        self.content = content
        self.liked_number = liked_number
        self.reply_number = reply_number
    def display(self):
        print(self.content+"--------"+self.user.name+" get "+str(self.liked_number)+" likes and "+ str(self.reply_number)+"reply")


class User(object):
    """docstring for User"""
    def __init__(self, id,name,description,url,touxiang_url,follower_number,follow_numebr):
        self.id = id
        self.name = name
        self.description = description
        self.url = url
        self.touxiang_url = touxiang_url
        self.follower_number = follower_number
        self.follow_numebr = follow_numebr
    def display(self):
        print("id: "+str(self.id)+" name: "+self.name+" description: "+self.description)


def parse_url(id,max_id=None,max_id_type=None):
    request_url = ""
    if max_id=="":
        request_url =  base_url_first.format(str(id))
        #print(request_url)
    else:
        request_url = base_url_others.format(str(id),str(max_id),str(max_id_type))
    return request_url

def parse_result(murl):
    r = requests.get(murl,headers)
    print(r.status_code)
    # print(r.text)
    result = json.loads(r.text)
    comment_lists = result["data"]["data"]
    length = len(comment_lists)
    #comment = comment_lists[1]
    for comment in comment_lists:
        #for key,value in comment.items():
            #print("key: "+str(key)+" value: "+str(value))
        userInfo = comment["user"]
        user = User(userInfo["id"],userInfo["screen_name"],userInfo["description"],userInfo["profile_url"],userInfo["profile_image_url"],
                    userInfo["followers_count"],userInfo["follow_count"])
        #user.display()
        content = comment["text"]
        liked_number = comment["like_count"]
        reply_number = comment["total_number"]
        #print(content+" "+str(liked_number)+" "+str(reply_number))
        mcomment = Comment(user,content,liked_number,reply_number)
        mcomment.display()

    max_id = result["data"]["max_id"]
    max_id_type = result["data"]["max_id_type"]
    return max_id,max_id_type



def main(weibo_url):
    id = weibo_url.split("/")[-1]  
    max_id_type = ""
    max_id = ""
    for i in range(0,10):
        request_url = parse_url(id,max_id,max_id_type)
        print("request_url="+request_url+'\n')
        max_id,max_id_type = parse_result(request_url)
        print("第"+str(i)+"次请求"+'\n')


if  __name__  ==  '__main__':
    weibo_url = "https://m.weibo.cn/detail/4391165086117795"
    main(weibo_url)
    