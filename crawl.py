from bs4 import BeautifulSoup
import requests
import csv


mobile_hdr = {'Accept-Language': 'ko_KR,en;q=0.8', 'User-Agent': (
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Mobile Safari/537.36')}
pc_hdr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
url = 'https://www.op.gg/champion/statistics'
req = requests.get(url, headers=mobile_hdr)
html = req.text
s = BeautifulSoup(html, 'html.parser')
# 시작
first = s.find("div", {"class": 'by-champion__wrapper by-champion__wrapper--champion-list'})
second = first.select_one('div')
ab = []
pos_rec = []
result_rec = []
rank = ["Best", "Excellent", "Great", "Nice", "Good"]
img_rank = ["../static/image/tier/challenger.png", "../static/image/tier/grandmaster.png", "../static/image/tier/master.png", "../static/image/tier/diamond.png", "../static/image/tier/platinum.png"]


for i, z in enumerate(['가렌', '갈리오', '갱플랭크', '엘리스', '다리우스']):
    count = []
    
    third = second.find('div', {"data-champion-name": z})
    fourth = third.select_one('a')['href']

    s_link = ('https://www.op.gg' + fourth)
    pc_answer = requests.get(s_link, headers=pc_hdr)
    pc_html = pc_answer.text

    pc_so = BeautifulSoup(pc_html, 'html.parser')
    pc_pic = pc_so.find("div", {"class": 'champion-box-content'})

    pc_rate = pc_pic.find_all('div', {'champion-stats-trend-rate'})

    pc_picrate = pc_rate[1].get_text().strip()
    pc_winrate = pc_rate[0].get_text().strip()

    s_answer = requests.get(s_link, headers=mobile_hdr)
    s_html_image = s_answer.text

    s_so = BeautifulSoup(s_html_image, 'html.parser')

    champ_src = s_so.select_one('div.champion__image > img')['src']

    s_img = s_so.find("table", {
        "class": 'matchup-summary__list matchup-summary__list--table tabItem ChampionMatchupSummaryTable-Strong'})
    
    for u in range(1, 4):
        ab = s_img.select_one('tr:nth-child(' + str(u) + ')> td > img')['src']
        count.append(ab)

    rec_champ_info = {
        'src':champ_src,
        'win':pc_winrate,
        'pick':pc_picrate,
        'counter_img':count
    }

    rec_champ_list = {
        'rank_img':img_rank[i],
        'rank': rank[i],
        'name': z,
        'info': rec_champ_info
    }
    result_rec.append(rec_champ_list)

f = open("./lol_chams.csv", mode="wt", encoding="cp949", newline='') 
# 끝
for lane in ['TOP', 'JUNGLE', 'MID', 'ADC', 'SUPPORT']:

    message = lane + ' 상위 5 챔피언\n'
    soup = s.find("div", {"class": "detail-ranking__content detail-ranking__content--champ-list ChampionRankingList-WinRatio-{} tabItem".format(lane)})
    paths = soup.select_one('ul')
    names = soup.find_all("div", {"class": "champion-ratio__name"})[:5]
    infos = soup.find_all("div", {"class": "champion-ratio__percent"})[:10]
    num = ['1st', '2nd', '3rd', '4th', '5th']

    for idx in range(1, 6):
        path = paths.select_one('li:nth-child(' + str(idx) + ')>a')['href']
        link = ('https://www.op.gg' + path)
        answer = requests.get(link, headers=mobile_hdr)
        html_image = answer.text
        so = BeautifulSoup(html_image, 'html.parser')
        soup_image = so.find("div", {"class": "champion tabWrap"})
        aa = soup_image.select_one('div > div > img')
        image_list = aa['src']

        champ = {'num': num[idx-1],
                'name': names[idx - 1].text.strip(),
                'win': infos[2 * (idx - 1)].text.strip().replace('\n', ' '),
                'pick': infos[2 * (idx - 1) + 1].text.strip().replace('\n', ' '),
                'img' : image_list}

        position = {'line': lane, 
                    'info': champ}

        pos_rec.append(position)
        writer = csv.writer(f) 
        writer.writerow([position]) 

    message += '\n'
f.close()