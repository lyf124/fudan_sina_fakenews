from lxml import etree
import  requests
import json
import js2xml

headers = {
    'authority': 'weibo.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'SINAGLOBAL=2417947650939.4717.1606714345953; wvr=6; UOR=,,www.baidu.com; SSOLoginState=1607066845; _s_tentry=login.sina.com.cn; Apache=1956371010333.098.1607066850218; ULV=1607066850653:3:2:3:1956371010333.098.1607066850218:1606816614627; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWPl0e-uYorHSdZ.Ksojh-M5JpX5KMhUgL.FozRSozR1he0ShB2dJLoIEXLxK.LB.zL1K2LxKqLBoBLBozLxK.L1-BL1--LxKBLB.2LB.2LxK-L1K2L1h5t; ALF=1638841802; SCF=AmHVvqqunNh90KhYoaMadC124GqarDaLrJOVyPdsULHyeqNruBzkCFAsVLn8JJDGc6lgbSunBwyxzDP7tvr2mAc.; SUB=_2A25yyfobDeRhGeRG7VAZ-C3PzziIHXVRv2zTrDV8PUNbmtCOLVbYkW9NUhx5-g4zLmkrjvBzId8jgQV5MvFqAfDV; wb_view_log_2862883344=1280*7201.5; webim_unReadCount=%7B%22time%22%3A1607305816315%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A29%2C%22msgbox%22%3A0%7D',
}

# request.setCharacterEncoding("UTF-8");


for i in range(1,460):
    url = 'https://weibo.com/cctvxinwen?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page={}#feedtop'.format(i)
    r = requests.get(url, headers=headers)
    # WB_text W_f14
    r.encoding = 'utf-8'

    response = etree.HTML(r.text)
    # print(r.text)
    script_list = response.xpath("//script/text()")
    filter_script = [script for script in script_list if
                     script.find('FM.view({"ns":"pl.content.homeFeed.index","domid":"Pl_Official_MyProfileFeed') != -1]
    # print(filter_script)
    try:
        script_text = js2xml.parse(filter_script[0], encoding='utf-8', debug=False)
        # print(script_list[-1])
        script_tree = js2xml.pretty_print(script_text)
        # print(script_tree)
        selector = etree.HTML(script_tree)
        div_selector = selector.xpath("//program//property[@name='html']/string/text()")[0]
        div_tree_se = etree.HTML(div_selector)
        text_selectors = div_tree_se.xpath("//div[@class='WB_text W_f14']")
        text_selectors_full = div_tree_se.xpath("//div[@node-type='feed_list_content_full']")
        print(text_selectors_full)
        for text_se in text_selectors:
            text = ''.join(text_se.xpath('./text()')).replace('\n', '').replace(' ', '')
            if (text.find('【') != -1 and text.find('】') != -1):
                text = text.split("】")[1]
            if (text[0] == '，' or text[0] == "？"):
                text = text[1:]
            if (len(text) < 10):
                continue
            print("news", text.replace("​", ''))
            with open("../data/yangshi_data.txt", "a", encoding="utf-8") as file:
                file.writelines(text.replace("​", '') + "\n")
    except:
        continue
