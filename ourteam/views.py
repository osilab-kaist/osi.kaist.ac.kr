from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.


def display_professor(request):
    data = {
        "menu_active": {
            "ourteam": "active"
        }
        ,
        'phd_list': [
            {"name": "Jung-Hun Kim", "email": "junghunkim@kaist.ac.kr", "period": " Industrial and System Engineering, 2018 Fall ~", "img": "images/members/junghoon.jpg"},
            {"name": "SangMook Kim", "email": "sangmook.kim@kaist.ac.kr", "period": "Knowledge Service Engineering, 2019 Spring ~", "img": "images/members/sangmook.jpg"},
            {"name": "Mingyu Kim", "email": "callingu@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": "images/members/mingyu.jpg"},
            {"name": "Narae Ryu", "email": "nrryu@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": ""},
            {"name": "Gihun Lee", "email": "opcrisis@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "images/members/gihun.jpg"},
            {"name": "Taehyeon Kim", "email": "potter32@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "images/members/taehyeon.jpg"},
            {"name": "Jongwoo Ko", "email": "jongwoo.ko@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": ""},
        ],
        'integrated_list':[
            {"name": "Jaehoon Oh", "email": "jhoon.oh@kaist.ac.kr", "period": "Knowledge Service Engineering, 2017 Fall ~", "img": "images/members/jaehoon.jpg"},
           {"name": "Seongyoon Kim", "email": "curisam@kaist.ac.kr", "period": "Industrial and System Engineering, 2018 Spring ~", "img": "images/members/seongyoon.jpg"},
        ],
        "ms_list": [
            {"name": "Hyungjun Yoo", "email": "yoohjun@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Fall ~",  "img": "images/members/hyungjun.jpg"},
            {"name": "Marseille Gauvain Jacques", "email": "marseilleg@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Fall ~",  "img": "images/members/gauvain.jpg"},
            {"name": "Sangmin Bae", "email": "bsmn0223@kaist.ac.kr", "period": "Industrial and System Engineering, 2019 Spring ~",  "img": "images/members/sangmin.jpg"},
            {"name": "Jonghyup Kim", "email": "leenams2@kaist.ac.kr", "period": "Industrial and System Engineering, 2019 Spring ~",  "img": "images/members/jonghyup.jpg"},
            {"name": "ChangHwan Kim", "email": "kimbob@kaist.ac.kr", "period": "Knowledge Service Engineering, 2019 Spring ~", "img": "images/members/changhwan.jpg"},
            {"name": "KyeongRyeol Go", "email": "kyeongryeol.go@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", 'img': ""},
            {"name": "Sungnyun Kim", "email": "ksn4397@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": ""},
            {"name": "Jinhwan Choi", "email": "jinhwanchoi@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": ""},
            {"name": "Sangwook Cho", "email": "sangwookcho@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": ""},
            {"name": "Nakyil Kim", "email": "nakyilkim@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": ""},
            {"name": "Jaeyeon Ahn", "email": "dkswodus49@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": ""},
        ]
    }

    return render(request, 'professor.html', data)


def display_students(request):
    data = {
        "menu_active": {
            "ourteam": "active"
        }
        ,
        'phd_list': [
            {"name": "Jung-Hun Kim", "email": "junghunkim@kaist.ac.kr", "period": " Industrial and System Engineering, 2018 Fall ~", "img": "images/members/junghoon.png"},
            {"name": "SangMook Kim", "email": "sangmook.kim@kaist.ac.kr", "period": "Graduate School of AI, 2019 Spring ~", "img": "images/members/sangmook.png"},
            {"name": "Mingyu Kim", "email": "callingu@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": "images/members/mingyu.png"},
            {"name": "Narae Ryu", "email": "nrryu@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": "images/members/narae.png"},
            {"name": "Gihun Lee", "email": "opcrisis@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "images/members/gihun.png"},
            {"name": "Taehyeon Kim", "email": "potter32@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "images/members/taehyeon.png"},
            {"name": "Jongwoo Ko", "email": "jongwoo.ko@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "images/members/jongwoo.png"},
            {"name": "Sangmin Bae", "email": "bsmn0223@kaist.ac.kr", "period": "Graduate School of AI, 2021 Spring ~",  "img": "images/members/sangmin.png"},
            {"name": "Sumyeong Ahn", "email": "sumyeongahn@kaist.ac.kr", "period": "Graduate School of AI, 2017 Spring ~",  "img": "images/members/sumyeong.jpeg"},
            {"name": "Sungnyun Kim", "email": "ksn4397@kaist.ac.kr", "period": "Graduate School of AI, 2021 Fall ~", "img": "images/members/sungnyun.jpg"},
        ],
        'integrated_list':[
            {"name": "Jaehoon Oh", "email": "jhoon.oh@kaist.ac.kr", "period": "Knowledge Service Engineering, 2017 Fall ~", "img": "images/members/jaehoon.png"},
            {"name": "Seongyoon Kim", "email": "curisam@kaist.ac.kr", "period": "Industrial and System Engineering, 2018 Spring ~", "img": "images/members/seongyoon.png"},
        ],
        "ms_list": [
            {"name": "Gahee Kim", "email": "gaheekim@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": "images/members/gahee.jpg"},
            {"name": "Nakyil Kim", "email": "nakyilkim@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "images/members/nakyil.png"},
            {"name": "Jihwan Oh", "email": "ericoh929@kaist.ac.kr", "period": "Graduate School of AI, 2021 Spring ~", "img": "images/members/jihwan.jpg"},
            {"name": "Jaewoo Shin", "email": "yimsungen5@kaist.ac.kr", "period": "Graduate School of AI, 2021 Spring ~", "img": "images/members/jaewoo.jpg"},
            {"name": "Donggyu Kim", "email": "eaststar@kaist.ac.kr", "period": "Graduate School of AI, 2021 Spring ~", "img": "images/members/donggyu.jpg"},
            {"name": "Minchan Jeong", "email": "mcjeong@kaist.ac.kr", "period": "Graduate School of AI, 2021 Spring ~", "img": "images/members/minchan.png"},
            {"name": "Seungjoon Park", "email": "sjoon.park@kaist.ac.kr", "period": "Graduate School of AI, 2021 Fall ~", "img": "images/members/seungjoon.jpg"},
            {"name": "Junghyun Lee", "email": "jh_lee00@kaist.ac.kr", "period": "Graduate School of AI, 2021 Fall ~", "img": "images/members/junghyun.jpeg"},
            {"name": "Namgyu Ho", "email": "itsnamgyu@kaist.ac.kr", "period": "Graduate School of AI, 2021 Fall ~", "img": "images/members/namgyu.jpg"},
        ]
    }

    return render(request, 'students.html', data)


def display_alumni(request):
    data = {
        "menu_active": {
            "ourteam": "active"
        },
        'ms_alumni_list': [
            {"name": "Jinhwan Choi", "email": "jinhwanchoi@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~ 2022 Spring", "img": "images/members/jinhwan.png"},
            {"name": "Sangwook Cho", "email": "sangwookcho@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~ 2022 Spring", "img": "images/members/sangwook.png"},
            {"name": "Jaeyeon Ahn", "email": "dkswodus49@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~ 2022 Spring", "img": "images/members/jaeyeon.JPG"},
            {"name": "KyeongRyeol Go", "email": "kyeongryeol.go@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~ 2021 Fall", 'img': "images/members/kyeongryeol.png", "job": "SPACEWALK"},
            {"name": "Sungnyun Kim", "email": "ksn4397@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~ 2021 Fall", "img": "images/members/sungnyun.jpg", 'job': "Ph.D. program in KAIST, AI graduate school" },
            {"name": "Sangmin Bae", "email": "bsmn0223@kaist.ac.kr", "period": "Industrial and System Engineering, 2019 Spring ~ 2021 Spring",  "img": "images/members/sangmin.png", 'job': "Ph.D. program in KAIST, AI graduate school"},
            {"name": "Jonghyup Kim", "email": "leenams2@kaist.ac.kr", "period": "Industrial and System Engineering, 2019 Spring ~ 2021 Spring",  "img": "images/members/jonghyup.png", "job": "Samsung"},
            {"name": "ChangHwan Kim", "email": "kimbob@kaist.ac.kr", "period": "Knowledge Service Engineering, 2019 Spring ~ 2021 Spring", "img": "images/members/changhwan.png", "job": "Tmax"},
            {"name": "Hyungjun Yoo", "email": "yoohjun@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Fall ~ 2021 Spring",  "img": "images/members/hyungjun.png", "job": "Samsung"},
            {"name": "Marseille Gauvain Jacques", "email": "marseilleg@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Fall ~ 2020 Fall",  "img": "images/members/gauvain.png", "job": ""},
            {"name": "Gihun Lee", "email": "opcrisis@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Spring ~ 2020 Spring", "img": "images/members/gihun.png", 'job': "Ph.D. program in KAIST, AI graduate school"},
            {"name": "Taehyeon Kim", "email": "potter32@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Spring ~ 2020 Spring", "img": "images/members/taehyeon.png", 'job': "Ph.D. program in KAIST, AI graduate school"},
            {"name": "SangMook Kim", "email": "sangmook.kim@kaist.ac.kr", "period": "Knowledge Service Engineering, 2017 Spring ~ 2019 Spring", "img": "images/members/sangmook.png", 'job': "Ph.D. program in KAIST, AI graduate school"},
            {"name": "Jung-Hun Kim", "email": "junghunkim@kaist.ac.kr", "period": "Knowledge Service Engineering, 2016 Fall ~ 2018 Fall", "img": "images/members/junghoon.png", 'job': "Ph.D. program in KAIST, ISysE"},
        ]
    }

    return render(request, 'alumni.html', data)
