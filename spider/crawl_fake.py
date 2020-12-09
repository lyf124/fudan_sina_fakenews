from lxml import etree
import  requests
import json
import js2xml
cookies = {
    'SINAGLOBAL': '2417947650939.4717.1606714345953',
    'wvr': '6',
    'UOR': ',,www.baidu.com',
    'SSOLoginState': '1607066845',
    '_s_tentry': 'login.sina.com.cn',
    'Apache': '1956371010333.098.1607066850218',
    'ULV': '1607066850653:3:2:3:1956371010333.098.1607066850218:1606816614627',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWPl0e-uYorHSdZ.Ksojh-M5JpX5KMhUgL.FozRSozR1he0ShB2dJLoIEXLxK.LB.zL1K2LxKqLBoBLBozLxK.L1-BL1--LxKBLB.2LB.2LxK-L1K2L1h5t',
    'ALF': '1638841802',
    'SCF': 'AmHVvqqunNh90KhYoaMadC124GqarDaLrJOVyPdsULHyeqNruBzkCFAsVLn8JJDGc6lgbSunBwyxzDP7tvr2mAc.',
    'SUB': '_2A25yyfobDeRhGeRG7VAZ-C3PzziIHXVRv2zTrDV8PUNbmtCOLVbYkW9NUhx5-g4zLmkrjvBzId8jgQV5MvFqAfDV',
    'webim_unReadCount': '%7B%22time%22%3A1607305887230%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A29%2C%22msgbox%22%3A0%7D',
    'S_ACCOUNT-G0': 'be88a4348fece2a046d63151b371dad1',
    'WBStorage': '8daec78e6a891122|undefined',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# request.setCharacterEncoding("UTF-8");
url = 'https://service.account.weibo.com/index?type=5&status=0&page=2'

for i in range(1,250):
    url ='https://service.account.weibo.com/index?type=5&status=0&page={}'.format(i)
    r = requests.get(url, headers=headers, cookies=cookies)

    r.encoding = 'utf-8'
    # print (r.text)
    response = etree.HTML(r.text)
    script_list = response.xpath('//script/text()')
    # print(script_list)

    # filter_script  = [ script for script in script_list if script.find('pl_service_showcomplaint')!=-1]
    script_text = js2xml.parse(script_list[-1], encoding='utf-8', debug=False)
    # print(script_list[-1])
    script_tree = js2xml.pretty_print(script_text)
    # print(script_tree)
    selector = etree.HTML(script_tree)
    div_selector = selector.xpath("//program//property[@name='html']/string/text()")[0]
    div_tree_se = etree.HTML(div_selector)

    url_list = div_tree_se.xpath("//div[@class='m_table_tit']/a/@href")
    for url in url_list:
        url_pre = "https://service.account.weibo.com"
        url_com = url_pre + url
        r = requests.get(url_com, headers=headers, cookies=cookies)
        response = etree.HTML(r.text)
        # print(r.text)
        script_list = response.xpath('//script/text()')
        filter_script = [script for script in script_list if script.find('pl_service_common') != -1]
        script_text = js2xml.parse(filter_script[0], encoding='utf-8', debug=False)

        script_tree = js2xml.pretty_print(script_text)
        # print(script_tree)
        selector = etree.HTML(script_tree)
        div_selector = selector.xpath("//program//property[@name='html']/string/text()")[0]
        div_tree_se = etree.HTML(div_selector)
        text = div_tree_se.xpath("//div[@class='feed bg_orange2 clearfix']/div[@class='con']/text()")
        try:
            text = \
            div_tree_se.xpath("//div[@class='feed bg_orange2 clearfix']/div[@class='con']/input/@value")[0].split(
                '<a title')[0].split(
                '<a href')[0]
        except:
            text = div_tree_se.xpath("//div[@class='feed bg_orange2 clearfix']/div[@class='con']/text()")[0].replace(
                "\n    \t    \t：", '')
        text = text.replace('\n', '').replace("​",'').replace(' ', '').strip()
        if (len(text) <= 8):
            # print(text,len(text))
            continue
        if (text.find('被举报人删除了被举报信息')!=-1 or text.find('<a')!=-1 or  text.find('<img')!=-1
                or text.find('<span')!=-1  or text.find('src')!=-1):
            continue

        print("news:", text, len(text))
        import re
        text = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", text)
        with open("../data/fake_data.txt", "a", encoding="utf-8") as file:
            file.writelines(text+"\n")


