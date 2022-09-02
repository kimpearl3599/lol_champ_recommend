
# LOL_CHAMP_RECOMMEND

Riot에서 제공하는 LOL Public API 데이터를 통해 Challenger ~ Platinum 까지의 상위권 구간 유저들의 most champion 데이터를 얻고 sklearn / cosine-similarity 를 활용하여 유사도 학습 진행

회원가입시 사용자의 실제 LOL 닉네임으로 가입을 유도하여 해당 유저정보를 op.gg에서 크롤링하여 most champion 데이터 수집
선행 학습된 데이터와 더불어 수집한 데이터를 바탕으로, 사용자와 most champion이 유사한 상위권 유저들이 애용하는 또다른 champion 추천

<br>

**Cosine-similarity evaluation**

[https://colab.research.google.com/drive/1qCf7ZhuGgrJIxayDX2kYZ9nbDm18CYJe](https://colab.research.google.com/drive/1qCf7ZhuGgrJIxayDX2kYZ9nbDm18CYJe)

<br>

## 프로젝트 개요
### 프로젝트명 : 롤 챔피언 추천 시스템 <LOL_CHAMP_RECOMMEND>

<br>

[시연 영상](https://youtu.be/V4Oq9yvqCp8) 👈 link <br>
### 개발기간
22.01.26(수) ~ 22.02.09(수)
10일간(기획 2일, 개발 8일)

### 전체일정 프로세스
1일차 : 프로젝트 기획(API설계, 와이어프레임작성), 기능 선정, 역할 분담, 기능별 html 제작<br>
2일차 : Mysql DB연결<br>
3일차 : 웹 크롤링기능 구현<br>
4일차 : 모델 구현<br>
5일차 : 모델기능 메인에 연결, 크롤링 마무리<br>
6일차 : 채팅기능 구현<br>
7일차 : 전체 페이지 수정<br>
8일차 : css 마무리<br>
9일차 : 페이지 연결하기, 리드미 작성<br>
10일차 : 영상촬영 및 발표<br>

<br>

## 서비스 기능

### 1. 메인 페이지
- 로그인 & 회원가입

### 2. 홈 페이지
- 챔피언 추천 시작 버튼을 눌러서 사용자에게 맞는 챔피언을 추천하여 결과를 보여줌
- op.gg사이트에서 각 라인별 챔피언 TOP5를 크롤링하여 보여줌
- 사용자가 팔로우한 유저를 불러와서 보여줌

### 3. 채팅 페이지
- 전체 유저리스트 중에 친구추가된 유저만 채팅이 가능
- 선택한 유저와 실시간 1:1 채팅이 가능
- 사용자가 작성한 글은 오른쪽에 선택한 유저가 작성한 글은 왼편에서 보여줌

<br>

## 구현기능
- 모델을 통하여 사용자 맞춤 챔피언 추천 기능
- 친구 팔로우 및 취소 기능
- 채팅기능
- 라인별TOP5 크롤링기능

<br>

## 사용도구
- HTML, CSS
- Javascript
- Python - django, Mysql, requests, sklearn, bs4
- colab pro
- AWS

<br>

### Collaboration & Tools
- Slack & gather
- Figma
- GIT / GIT Hub

<br>

## 팀빌딩 및 역할
- 부트캠프 <스파르타 내일배움캠프> 참가자로 구성

### 개발자 (가나다순)<br>
**김재명 @mungnpang**<br>
✔️ 프론트엔드 총괄<br>
✔️ 추천 시스템 구현<br>
✔️ 페이지별 오류 수정<br>
<br>
**김진주 @kimpearl3599**<br>
✔️ 채팅페이지 기능 및 css<br>
✔️ Git, Github 관리<br>
✔️ 모델 구현<br>
<br>
**김한석 @novahope**<br>
✔️ 일러스트 및 영상 제작<br>
✔️ 모델 구현<br>
✔️ 발표<br>
<br>
**이병준 @dugadak**<br>
✔️ 장고 API 설계 및 구현<br>
✔️ 크롤링 기능 및 수정<br>
✔️ DB 연결 및 관리<br>
<br>
**전승현 @kidcode**<br>
✔️ 장고 API 설계 및 구현<br>
✔️ 크롤링 기능 및 수정<br>
✔️ DB 연결 및 관리<br>

<br>

## API소개
https://www.notion.so/LOL_CHAMP_RECOMMEND-1070e5ff4d6b4b3da5970eefa3dc06e1<br>
![image](https://user-images.githubusercontent.com/79038451/153117530-0392b563-539e-46a7-9c7e-b1d90ff8116b.png)
![image](https://user-images.githubusercontent.com/79038451/153117482-06ac5650-77fc-4209-9e55-10c468f1320b.png)
![image](https://user-images.githubusercontent.com/79038451/153117505-7bd76bea-20e9-4e6a-b914-c9df451c6d46.png)


## Workflow
https://www.figma.com/file/koFxHBPNePCQsSBFXBbUhc/Untitled?node-id=4%3A6<br>
![image](https://user-images.githubusercontent.com/79038451/153117548-0d996427-b12e-42b2-9c40-309855a14b09.png)




