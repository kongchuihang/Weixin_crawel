from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import re
base_url='https://weixin.sogou.com/weixin?'
headers={
'Cookie':'CXID=C4DEFAE9DFCAF879043832FF2A26CAE6; SUID=D7E3026A5E68860A5C2EF1090000B5C4; IPLOC=CN1100; SUV=0053D4546A02E3D75C355852B114C803; ad=4yllllllll2tas9JlllllVe6@Ullllllzka0CZllllwlllllROxlw@@@@@@@@@@@; pgv_pvi=3229553664; ABTEST=0|1550469603|v1; weixinIndexVisited=1; ppinf=5|1550470551|1551680151|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo1NDolRTUlOTglQkYlRUYlQkMlOEMlRTglQUYlQjclRTclQUQlODklRTQlQjglODAlRTQlQjglOEJ8Y3J0OjEwOjE1NTA0NzA1NTF8cmVmbmljazo1NDolRTUlOTglQkYlRUYlQkMlOEMlRTglQUYlQjclRTclQUQlODklRTQlQjglODAlRTQlQjglOEJ8dXNlcmlkOjQ0Om85dDJsdVA5ZVdtN1hEaUkyM2pVa2hfSHYyWFlAd2VpeGluLnNvaHUuY29tfA; pprdig=rfB9hJuGQkYWXmAkD631AkWv3WQmG320CjolUDCZlGIVGTQU1KUFiYtsEavwG_L1yUMYa273wCfbCE8RVrljBmJd4x9rLvL9IrhAhTe3pZFPSxjEZHfXvTkDBByKHH4LLageGjWwBIHDbhyaGEhoRO95vMoaJTv15TYS_ajcwZw; sgid=19-39361615-AVxqTZeAaWr8u6fzsM14VyM; ld=Dyllllllll2tz6$hlllllVerWUwlllllzka0CZllll9lllll9Zlll5@@@@@@@@@@; LSTMV=485%2C75; LCLKINT=1701; JSESSIONID=aaaRTPlCqY_Wcd0QcB6Hw; PHPSESSID=8a907u5kg15o2cgse5lpsjkfq0; ppmdig=1550566440000000f85adf2a43bcf2aed4f2a6688b7ef984; SNUID=90AB4A22484DCA7CC53BBF15487E7E32; seccodeRight=success; successCount=2|Tue, 19 Feb 2019 09:04:46 GMT; sct=12',
'Host': 'weixin.sogou.com',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
}
proxy=None
max_count=5
proxy_pool_url='http://localhost:5000/get'
proxies={}
title_list={
    'title':[],
    'content':[],
}
def get_proxy():
    try:
        response=requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
def get_html(url,count=1):
    print('Crawing',url)
    print('Tring Count',count)
    global proxy
    global proxies
    if count>= max_count:
        print('请求次数太多了')
        return None
    try:
        if proxy:
            # 设置代理
            proxies={
                'http':'http://'+proxy
            }
        #allow_redirects=False 不让它自动跳转 proxies 代理
        response=requests.get(url,allow_redirects=False,headers=headers,proxies=proxies)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print('302')
            proxy=get_proxy()
            if proxy:
                print('Using Proxy',proxy)
                count+=1
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error',e.args)
        proxy=get_proxy()
        count+=1
        return get_html(url,count)
def get_index(keyword,page):
    data={
        'query':keyword,
        'type': 2,
        'page':page,
        'ie': 'utf8'
    }
    # 把字典进行编码 变成以 get请求参数的类型
    queries=urlencode(data)
    url=base_url+queries
    html=get_html(url)
    return html
# 解析
def parse_index(html):
    soup=BeautifulSoup(html, features = 'html.parser')
    # 标题
    title = soup.select('a[data-share]')
    for title in title:
        title = title.text
        title_list['title'].append(title)
    # 内容
    content = soup.find_all('p', attrs={'id': re.compile(r'^sogou_vr')})
    for content in content:
        content = content.text
        title_list['content'].append(content)
    for i in range(0, len(title_list['title'])):
        print('title', title_list['title'][i].encode('UTF-8','ignore').decode('UTF-8'))
        print('content', title_list['content'][i].encode('UTF-8','ignore').decode('UTF-8'))
        print('另一个标题内容')

def main():
    for page1 in range(1,100):
        html=get_index('优美的句子',page1)
        parse_index(html)
if __name__ == '__main__':
    main()

