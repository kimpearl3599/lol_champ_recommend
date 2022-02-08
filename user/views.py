from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import json, requests
import csv
import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



def find_most(nickname):
    header = {'Accept-Language': 'ko_KR,en;q=0.8', 'User-Agent': ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Mobile Safari/537.36')}
    user = requests.get(f'https://www.op.gg/summoner/userName={nickname}', headers=header)
    # print(user)
    soup = BeautifulSoup(user.text, 'html.parser')
    # print(soup)
    ur_most_list = soup.find_all("div", attrs={"class":"ChampionName"})
    # print(ur_most_list)
    most_list = []

    for most in ur_most_list:
        most_list.append(most.select_one('a')['href'].split('/')[2])
    # print(most_list)
    return most_list

# @login_required
def home(request):
    user = request.user.is_authenticated
    home_user_id = request.user.id
    user_email= UserModel.objects.get(id=home_user_id)
    result = []
    
    # 챔피언 추천 부분
    if request.method == 'POST':
        nickname = user_email.nickname
        most_list = find_most(nickname)
        
        f = open("./user_most.csv", mode="wt", encoding="cp949", newline='')
        writer = csv.writer(f)

        writer.writerow(['userId', 'Champions', 'Rating']) 

        # 닉변의 변수
        if most_list is not None: 
            rating = float(5)
            for champ in most_list: 
                writer.writerow([nickname, champ, rating]) 
                rating -= 0.5

        f.close()
        
        # high ranker + mostlist -> cosine similarity을 이용해서 챔피언 풀이 비슷한 유저들을 찾아줌.
        highrank = pd.read_csv('./highrank.csv', encoding='cp949')
        champs = pd.read_csv('./lol_champs.csv')
        user_most = pd.read_csv('./user_most.csv', encoding="cp949")
        merged = pd.concat([highrank, user_most])
        # print(merged)

        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', 300)


        champs_ratings = pd.merge(merged, champs, on='Champions')
        user_favorite = champs_ratings.pivot_table('Rating', index='userId', columns='Champions')
        user_favorite = user_favorite.fillna(0)
        user_based_collab = cosine_similarity(user_favorite, user_favorite)
        user_based_collab = pd.DataFrame(user_based_collab, index=user_favorite.index, columns=user_favorite.index)
        
        recom_list = []
        for i in range(0, 10):
            users = user_based_collab[nickname].sort_values(ascending=False)[:10].index[i]
            # 지림
            # print(users)
            most_result = find_most(users)
            # print(most_result)
            for z in most_result:

                if z not in most_list:
                    recom_list.append(z)
        recom_result = recom_list[:5]

        
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

        for i, z in enumerate(recom_result):
            count = []
            
            third = second.find('div', {"data-champion-key": z})
            champs_ko_name = third.find('div', {"by-champion__item-name"}).get_text()

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
                'name': champs_ko_name,
                'info': rec_champ_info
            }
            result_rec.append(rec_champ_list)

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
            message += '\n'
        # print(result_rec)
        # print(count)
        
        user = request.user.is_authenticated
        if user:
            return render(request, 'home.html', {'crawling': pos_rec, 'result_rec':result_rec})
        else:
            return redirect('/')

    else:
        f = open('./lol_chams.csv', encoding='cp949')
        
        rdr = csv.reader(f)
        for line in rdr: 
            json_test = json.loads(line[0].replace("'", '"'))
            # print(json_test)
            result.append(json_test)

        user = request.user.is_authenticated
        id_name = request.user.id
        compare_user = UserModel.objects.get(id=id_name)
        
        if user:
            if request.method == 'GET':
                compare = compare_user.follow.all()

            return render(request, 'home.html', {'crawling':result, 'user_list': compare})
        else:
            return redirect('/')



def sign_in(request):
    sign_up(request)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # DB에 저장되어 있는 암호화되어있는 비밀번호와 내가 로그인하려는 정보의 비밀번호가 갖는지 알기위해 authenticate()메소드를 활용한다.
        me = auth.authenticate(request, username=username, password=password)

        if me is not None:
            auth.login(request, me)
            return redirect('/home')
        else:
            return render(request, 'entrance.html', {'error': '유저이름 혹은 패스워드를 확인 해 주세요.'})

    elif request.method == 'GET':
        user = request.user.is_authenticated

        if user:
            return redirect('/home')

        else:
            return render(request, 'entrance.html')


def sign_up(request):
    if request.method == 'GET':
        # 로그인한 사용자가 다시 로그인한 화면이나 회원가입화면으로 가는 것을 방지하기 위해 작업을 해줘야 함.
        # 로그인한 사용자를 처리해주는 is_authenticated메소드를 사용하여 그것을 user변수에 저장
        user = request.user.is_authenticated
        # 만약 로그인한 사용자라면 기본페이지로 가게 함.
        if user:
            return redirect('/home')
        # 로그인한 상태가 아니라면 회원가입 페이지로 가게끔 함.
        else:
            return render(request, 'user/signup.html')

    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        nickname = request.POST.get('nickname', '')

        if password != password2:
            # 패스워드가 같지 않다고 알림
            return render(request, 'entrance.html', {'error': '패스워드를 확인 해 주세요.'})
        else:
            # 만약 유저네임과 비밀번호 둘중하나라도 공란이라면 
            if username == '' or password == '':
                return render(request, 'entrance.html', {'error': '이름과 비밀번호를 입력 해 주세요.'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                # 다시 회원가입 페이지를 띄워준다.
                return render(request, 'entrance.html', {'error': '이미 존재하는 아이디입니다.'})
            # 중복되는 아이디가 없다면     
            else:
                UserModel.objects.create_user(username=username, password=password, nickname=nickname)
                return redirect('/')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        # 나를 제외한 사용자의 리스트를 갖고온다.
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'home.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    # 로그인한 사용자
    me = request.user
    # 내가 방금 팔로우 누른 사람
    click_user = UserModel.objects.get(id=id)
    # 내가 팔로우한 사람의 모든 사람중에서 이미 내가 있다면
    if me in click_user.followee.all():
        # 팔로우에서 나를 제거해줘라
        click_user.followee.remove(request.user)
    else:
        # 그게 아니라면 추가해줘라
        click_user.followee.add(request.user)
    return redirect('/user')


