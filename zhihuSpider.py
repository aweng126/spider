import os
import re
from urllib import request
import requests, time
from bs4 import BeautifulSoup
from http import cookiejar
from PIL import Image

session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
}
try:
    # 从本地文件加载cookies
    # ignore_discard的意思是即使cookies将被丢弃也将它保存下来，ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
    session.cookies.load(ignore_discard=True)
except Exception as e:
    print('exception:', e)
    print('还没有cookie信息')


# 得到验证参数
def get_xsrf():
    url = 'https://www.zhihu.com'
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    tag = soup.find('input', attrs={'name': '_xsrf'})
    return tag['value']


# 得到验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    response = session.get(captcha_url, headers=headers)
    captcha_name = 'captcha.gif'
    with open(captcha_name, 'wb') as f:
        f.write(response.content)
    im = Image.open(captcha_name)
    im.show()
    return input('请输入验证码: ')

# 得到登录邮箱
def get_email():
    return  input('请输入账号')

# 得到登录密码
def get_password():
    return input('请输入密码')

# 登录
def login(email, password, _xsrf, captcha):
    data = {
        '_xsrf': _xsrf,
        'password': password,
        'email': email,
        'captcha': captcha
    }
    login_url = 'https://www.zhihu.com/login/email'
    response = session.post(login_url, data=data, headers=headers)
    print('response.json() =', response.json())
    # 保存cookies到本地
    session.cookies.save()


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    # 这里重定向一定要设置为false, 否则就算没有登录会被重定向到登录的地址去, 然后code就返回200了
    response = session.get(url, headers=headers, allow_redirects=False)
    code = response.status_code
    if code == 200:
        return True
    else:
        return False

'''
@question_num   知乎问题的编号
@answer_offset  回答的偏移量(从第几个答案开始)
@answer_limit   回答的限制数（本次返回多少个答案）
'''
def get_all_pic_url(question_num, answer_offset,answer_limit):
    url = 'https://www.zhihu.com/api/v4/questions/{qnum}/answers?include=data%5B*%5D.is_normal%2Cis_collapsed%2Cannotation_action%' \
          '2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%' \
          '2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&' \
          'offset={offset}&limit={limit}&sort_by=default'
    response = session.get(url.format(qnum=question_num,offset=answer_offset,limit=answer_limit), headers=headers, allow_redirects=False)
    json_response = response.json()
    answer = json_response['data']
    pattern = re.compile(r'data-original=\"https\:(.*?)\.(jpg|png)"')
    urls = [];
    for i in range(0, len(answer)):
        per_answer_dict = answer[i]  # dict
        per_answer_content_str = per_answer_dict['content']
        match = pattern.findall(per_answer_content_str)
        urls.extend(["https:" + i[0] + ".jpg" for i in match[1::2]])
    return urls

'''
@img_url 要下载图片的地址
@file_name  图片的名字
@folder_name 文件夹的名字
@folder_base  文件夹的基地址
'''
def download_url_picture(img_url, file_name, folder_name, folder_base):
    try:
        file_path = folder_base + '/' + folder_name
        if not os.path.exists(file_path):
            print('文件夹', file_path, '不存在，重新建立')
            os.makedirs(file_path)
        # 获得图片后缀
        file_suffix = os.path.splitext(img_url)[1]
        # 拼接图片名（包含路径）
        filename = '{}{}{}{}'.format(file_path, os.sep, file_name, file_suffix)
        # 下载图片，并保存到文件夹中
        request.urlretrieve(img_url, filename=filename)
    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        print('错误 ：', e)

'''
@qustion_num:知乎的问题号
@answer_num:想下载的回答数
@folder_name:文件夹名字
@folder_base:文件夹所在位置
'''
def start_kanmeizi(question_num,answer_offset, answer_limit, folder_name, folder_base):
    urls = get_all_pic_url(question_num, answer_offset,answer_limit)
    for i in range(0, len(urls)):
        download_url_picture(urls[i], folder_name + '('+str(i)+')', folder_name, folder_base)
        print(folder_name,'第', i, '张图片已经下载完成')


if __name__ == '__main__':
    file_base = 'C:\\Users\kingwen\Desktop'
    if isLogin():
        print('您已经登录')
    else:
        email = get_email()
        password = get_password()
        _xsrf = get_xsrf()
        print('_xsrf =', _xsrf)
        captcha = get_captcha()
        login(email, password, _xsrf, captcha)
    start_kanmeizi(39655195,-1, 20, '如何拍出不错的旅行风景照片？', file_base)
