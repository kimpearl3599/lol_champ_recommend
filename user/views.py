from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # DB에 저장되어 있는 암호화되어있는 비밀번호와 내가 로그인하려는 정보의 비밀번호가 갖는지 알기위해 authenticate()메소드를 활용한다.
        me = auth.authenticate(request, username=username, password=password)

        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error':'유저이름 혹은 패스워드를 확인 해 주세요.'})
        
    elif request.method == 'GET':
        user = request.user.is_authenticated

        if user:
            return redirect('/')

        else: 
            return render(request, 'user/signin.html')


def sign_up(request):
    if request.method == 'GET':
        # 로그인한 사용자가 다시 로그인한 화면이나 회원가입화면으로 가는 것을 방지하기 위해 작업을 해줘야 함.
        # 로그인한 사용자를 처리해주는 is_authenticated메소드를 사용하여 그것을 user변수에 저장
        user = request.user.is_authenticated
        # 만약 로그인한 사용자라면 기본페이지로 가게 함.
        if user:
            return redirect('/')
        # 로그인한 상태가 아니라면 회원가입 페이지로 가게끔 함.
        else:
            return render(request, 'user/signup.html')

    elif request.method == 'POST':
        username = request.POST.get('username', '') 
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            # 패스워드가 같지 않다고 알림
            return render(request, 'user/signup.html', {'error':'패스워드를 확인 해 주세요.'})
        else:
            # 만약 유저네임과 비밀번호 둘중하나라도 공란이라면 
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error':'이름과 비밀번호를 입력 해 주세요.'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                # 다시 회원가입 페이지를 띄워준다.
                return render(request, 'user/signup.html', {'error':'이미 존재하는 아이디입니다.'})
            # 중복되는 아이디가 없다면     
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/sign-in')


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        # 나를 제외한 사용자의 리스트를 갖고온다.
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


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