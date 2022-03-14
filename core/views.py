import os

from django.shortcuts import render
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from django.templatetags.static import static

from osilab_homepage.settings import PROJECT_DIR


def home(request):
    data = {
        "project_list": [
            {'title': "Development of XAI-based Technology for Smart Energe Platform",
             "detail": "This project aims at KEPCO to form a cluster of five schools including KAIST to propose XAI-based smart energy platform technology. In our lab, we study to solve bottlenecks caused by gradient sharing that occurs when training deep learning models with large amounts of data. To solve this problem, we compress the gradient using methods such as Random Projection and Sequential Trasmitting Method.",
             "img": "core/images/project/proj_kepco.png"},
            {'title': "AutoML",
             "detail": "The neural architecture search (NAS) has been a great success in a variety of applications such as image classification and natural language processing. Despite huge success, it faces a challenge that takes too much resource budgets (e.g.,  computational costs and storage), which stems from the vastness of NAS's search space. In this project, we aim to reduce the tremendous resource budget required due to the large search space.",
             "img": "core/images/project/proj_etri.png"},
            {'title': "Developing Models for Predicting Properties of Compounds using Artificial Neural Network",
             'detail': "Properties of tire compounds are closely related to the performance of tire. Therefore, one of the goals of this project is to develop models to predict properties of the compounds. Moreover, we aim to develop inverse design models to suggest proper compounds for the target properties. We also propose automatic systems for building AI models.",
             "img": "core/images/project/proj_hankooktire.png"},
            {'title': "Explainable intelligent system for optimal strategy in battles",
             'detail': "Recently, artificial neural networks have shown remarkable successes with huge datasets. However, with scarce data, artificial neural networks are terrible.  In military situations, unfortunately, it is difficult to obtain a large training dataset.  Military cases also require to explain the decisions that the algorithm generates, which is very tricky with general artificial neural networks. In this project, we address these problems and design new approaches using Bayesian frameworks.",
             "img": "core/images/project/proj_add.png"},
            {'title': "Alpha Weather",
             'detail': "This project aims to solve the short-term prediction of precipitation(rainfall) in 6 hours. Although many meteorologists have provided a reasonably accurate forecast of long-term precipitation, the short-term prediction remains a big challenge. We anticipate an accurate short-term prediction by using artificial intelligence like AlphaGo. In this project, we define useful input data to be utilized for the short-term precipitation and propose machine learning algorithms predicting short-term rainfalls.",
             "img": "core/images/project/proj_weather.png"},
            {'title': "Efficient Representation Learning Algorithm for Unlabeled Data",
             'detail': "We often unavailable to obtain enough labeled data for our target task(ex. Image Classification) in most real-world cases. Some recent works address the data shortage by proposing un-, semi-, or self- supervised learning methods that utilize unlabeled data to improve the performance in target task without or with only a few amounts of labeled data. In this project, we extend those methods to build a data and training efficient algorithm to cope with various real-world constraints. We start by vision data and then consider sequential data.",
             "img": "core/images/project/proj_hynix.png"},
        ]
    }

    return render(request, 'core/home.html', data)


def display_professor(request):
    data = {
        "menu_active": {
            "ourteam": "active"
        }
        ,
        'phd_list': [
            {"name": "Jung-Hun Kim", "email": "junghunkim@kaist.ac.kr", "period": " Industrial and System Engineering, 2018 Fall ~", "img": "core/images/members/junghoon.jpg"},
            {"name": "SangMook Kim", "email": "sangmook.kim@kaist.ac.kr", "period": "Knowledge Service Engineering, 2019 Spring ~", "img": "core/images/members/sangmook.jpg"},
            {"name": "Mingyu Kim", "email": "callingu@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": "core/images/members/mingyu.jpg"},
            {"name": "Narae Ryu", "email": "nrryu@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": "core/"},
            {"name": "Gihun Lee", "email": "opcrisis@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/images/members/gihun.jpg"},
            {"name": "Taehyeon Kim", "email": "potter32@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/images/members/taehyeon.jpg"},
            {"name": "Jongwoo Ko", "email": "jongwoo.ko@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/"},
        ],
        'integrated_list':[
            {"name": "Jaehoon Oh", "email": "jhoon.oh@kaist.ac.kr", "period": "Knowledge Service Engineering, 2017 Fall ~", "img": "core/images/members/jaehoon.jpg"},
           {"name": "Seongyoon Kim", "email": "curisam@kaist.ac.kr", "period": "Industrial and System Engineering, 2018 Spring ~", "img": "core/images/members/seongyoon.jpg"},
        ],
        "ms_list": [
            {"name": "Hyungjun Yoo", "email": "yoohjun@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Fall ~",  "img": "core/images/members/hyungjun.jpg"},
            {"name": "Marseille Gauvain Jacques", "email": "marseilleg@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Fall ~",  "img": "core/images/members/gauvain.jpg"},
            {"name": "Sangmin Bae", "email": "bsmn0223@kaist.ac.kr", "period": "Industrial and System Engineering, 2019 Spring ~",  "img": "core/images/members/sangmin.jpg"},
            {"name": "Jonghyup Kim", "email": "leenams2@kaist.ac.kr", "period": "Industrial and System Engineering, 2019 Spring ~",  "img": "core/images/members/jonghyup.jpg"},
            {"name": "ChangHwan Kim", "email": "kimbob@kaist.ac.kr", "period": "Knowledge Service Engineering, 2019 Spring ~", "img": "core/images/members/changhwan.jpg"},
            {"name": "KyeongRyeol Go", "email": "kyeongryeol.go@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", 'img': ""},
            {"name": "Sungnyun Kim", "email": "ksn4397@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": "core/"},
            {"name": "Jinhwan Choi", "email": "jinhwanchoi@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/"},
            {"name": "Sangwook Cho", "email": "sangwookcho@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/"},
            {"name": "Nakyil Kim", "email": "nakyilkim@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/"},
            {"name": "Jaeyeon Ahn", "email": "dkswodus49@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/"},
        ]
    }

    return render(request, 'core/professor.html', data)


def display_students(request):
    data = {
        "menu_active": {
            "ourteam": "active"
        }
        ,
        'phd_list': [
            {"name": "Jung-Hun Kim", "email": "junghunkim@kaist.ac.kr", "period": " Industrial and System Engineering, 2018 Fall ~", "img": "core/images/members/junghoon.png"},
            {"name": "SangMook Kim", "email": "sangmook.kim@kaist.ac.kr", "period": "Graduate School of AI, 2019 Spring ~", "img": "core/images/members/sangmook.png"},
            {"name": "Mingyu Kim", "email": "callingu@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": "core/images/members/mingyu.png"},
            {"name": "Narae Ryu", "email": "nrryu@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": "core/images/members/narae.png"},
            {"name": "Gihun Lee", "email": "opcrisis@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/images/members/gihun.png"},
            {"name": "Taehyeon Kim", "email": "potter32@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/images/members/taehyeon.png"},
            {"name": "Jongwoo Ko", "email": "jongwoo.ko@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/images/members/jongwoo.png"},
            {"name": "Sangmin Bae", "email": "bsmn0223@kaist.ac.kr", "period": "Graduate School of AI, 2021 Spring ~",  "img": "core/images/members/sangmin.png"},
            {"name": "Sumyeong Ahn", "email": "sumyeongahn@kaist.ac.kr", "period": "Graduate School of AI, 2017 Spring ~",  "img": "core/images/members/sumyeong.jpeg"},
            {"name": "Sungnyun Kim", "email": "ksn4397@kaist.ac.kr", "period": "Graduate School of AI, 2021 Fall ~", "img": "core/images/members/sungnyun.jpg"},
        ],
        'integrated_list':[
            {"name": "Jaehoon Oh", "email": "jhoon.oh@kaist.ac.kr", "period": "Knowledge Service Engineering, 2017 Fall ~", "img": "core/images/members/jaehoon.png"},
            {"name": "Seongyoon Kim", "email": "curisam@kaist.ac.kr", "period": "Industrial and System Engineering, 2018 Spring ~", "img": "core/images/members/seongyoon.png"},
        ],
        "ms_list": [
            {"name": "Gahee Kim", "email": "gaheekim@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~", "img": "core/images/members/gahee.jpg"},
            {"name": "Nakyil Kim", "email": "nakyilkim@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~", "img": "core/images/members/nakyil.png"},
            {"name": "Jihwan Oh", "email": "ericoh929@kaist.ac.kr", "period": "Graduate School of AI, 2021 Spring ~", "img": "core/images/members/jihwan.jpg"},
            {"name": "Jaewoo Shin", "email": "yimsungen5@kaist.ac.kr", "period": "Graduate School of AI, 2021 Spring ~", "img": "core/images/members/jaewoo.jpg"},
            {"name": "Donggyu Kim", "email": "eaststar@kaist.ac.kr", "period": "Graduate School of AI, 2021 Spring ~", "img": "core/images/members/donggyu.jpg"},
            {"name": "Minchan Jeong", "email": "mcjeong@kaist.ac.kr", "period": "Graduate School of AI, 2021 Spring ~", "img": "core/images/members/minchan.png"},
            {"name": "Seungjoon Park", "email": "sjoon.park@kaist.ac.kr", "period": "Graduate School of AI, 2021 Fall ~", "img": "core/images/members/seungjoon.jpg"},
            {"name": "Junghyun Lee", "email": "jh_lee00@kaist.ac.kr", "period": "Graduate School of AI, 2021 Fall ~", "img": "core/images/members/junghyun.jpeg"},
            {"name": "Namgyu Ho", "email": "itsnamgyu@kaist.ac.kr", "period": "Graduate School of AI, 2021 Fall ~", "img": "core/images/members/namgyu.jpg"},
        ]
    }

    return render(request, 'core/students.html', data)


def display_alumni(request):
    data = {
        "menu_active": {
            "ourteam": "active"
        },
        'ms_alumni_list': [
            {"name": "Jinhwan Choi", "email": "jinhwanchoi@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~ 2022 Spring", "img": "core/images/members/jinhwan.png"},
            {"name": "Sangwook Cho", "email": "sangwookcho@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~ 2022 Spring", "img": "core/images/members/sangwook.png"},
            {"name": "Jaeyeon Ahn", "email": "dkswodus49@kaist.ac.kr", "period": "Graduate School of AI, 2020 Spring ~ 2022 Spring", "img": "core/images/members/jaeyeon.JPG"},
            {"name": "KyeongRyeol Go", "email": "kyeongryeol.go@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~ 2021 Fall", 'img': "images/members/kyeongryeol.png", "job": "SPACEWALK"},
            {"name": "Sungnyun Kim", "email": "ksn4397@kaist.ac.kr", "period": "Graduate School of AI, 2019 Fall ~ 2021 Fall", "img": "core/images/members/sungnyun.jpg", 'job': "Ph.D. program in KAIST, AI graduate school" },
            {"name": "Sangmin Bae", "email": "bsmn0223@kaist.ac.kr", "period": "Industrial and System Engineering, 2019 Spring ~ 2021 Spring",  "img": "core/images/members/sangmin.png", 'job': "Ph.D. program in KAIST, AI graduate school"},
            {"name": "Jonghyup Kim", "email": "leenams2@kaist.ac.kr", "period": "Industrial and System Engineering, 2019 Spring ~ 2021 Spring",  "img": "core/images/members/jonghyup.png", "job": "Samsung"},
            {"name": "ChangHwan Kim", "email": "kimbob@kaist.ac.kr", "period": "Knowledge Service Engineering, 2019 Spring ~ 2021 Spring", "img": "core/images/members/changhwan.png", "job": "Tmax"},
            {"name": "Hyungjun Yoo", "email": "yoohjun@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Fall ~ 2021 Spring",  "img": "core/images/members/hyungjun.png", "job": "Samsung"},
            {"name": "Marseille Gauvain Jacques", "email": "marseilleg@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Fall ~ 2020 Fall",  "img": "core/images/members/gauvain.png", "job": ""},
            {"name": "Gihun Lee", "email": "opcrisis@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Spring ~ 2020 Spring", "img": "core/images/members/gihun.png", 'job': "Ph.D. program in KAIST, AI graduate school"},
            {"name": "Taehyeon Kim", "email": "potter32@kaist.ac.kr", "period": "Knowledge Service Engineering, 2018 Spring ~ 2020 Spring", "img": "core/images/members/taehyeon.png", 'job': "Ph.D. program in KAIST, AI graduate school"},
            {"name": "SangMook Kim", "email": "sangmook.kim@kaist.ac.kr", "period": "Knowledge Service Engineering, 2017 Spring ~ 2019 Spring", "img": "core/images/members/sangmook.png", 'job': "Ph.D. program in KAIST, AI graduate school"},
            {"name": "Jung-Hun Kim", "email": "junghunkim@kaist.ac.kr", "period": "Knowledge Service Engineering, 2016 Fall ~ 2018 Fall", "img": "core/images/members/junghoon.png", 'job': "Ph.D. program in KAIST, ISysE"},
        ]
    }

    return render(request, 'core/alumni.html', data)


def photo(request, year):
    main_path = os.path.join(PROJECT_DIR, "core/static/core/images/photo/")

    photo_data = {
        2019: [f for f in listdir(main_path + "2019") if isfile(join(main_path + "2019", f))],
        2020: [f for f in listdir(main_path + "2020") if isfile(join(main_path + "2020", f))],
        2021: [f for f in listdir(main_path + "2021") if isfile(join(main_path + "2021", f))]
    }

    data = {
        "menu_active": {
            "photo": "active"
        },
    }

    data['photo_lst'] = photo_data[year]
    data['year'] = year

    return render(request, 'core/photo.html', data)


def ongoing_projects(request):
    data = {
        "menu_active": {
            "projects": "active"
        },

        "project_list": [
            {'title': "AutoML", "detail": "The neural architecture search (NAS) has been a great success in a variety of applications such as image classification and natural language processing. Despite huge success, it faces a challenge that takes too much resource budgets (e.g.,  computational costs and storage), which stems from the vastness of NAS's search space. In this project, we aim to reduce the tremendous resource budget required due to the large search space.", "img": "core/images/project/proj_etri.png"},
            {'title': "Developing Models for Predicting Properties of Compounds using Artificial Neural Network", 'detail': "Properties of tire compounds are closely related to the performance of tire. Therefore, one of the goals of this project is to develop models to predict properties of the compounds. Moreover, we aim to develop inverse design models to suggest proper compounds for the target properties. We also propose automatic systems for building AI models.",  "img": "core/images/project/proj_hankooktire.png"},
            {'title': "Explainable intelligent system for optimal strategy in battles", 'detail': "Recently, artificial neural networks have shown remarkable successes with huge datasets. However, with scarce data, artificial neural networks are terrible.  In military situations, unfortunately, it is difficult to obtain a large training dataset.  Military cases also require to explain the decisions that the algorithm generates, which is very tricky with general artificial neural networks. In this project, we address these problems and design new approaches using Bayesian frameworks.",  "img": "core/images/project/proj_add.png"},
            {'title': "Alpha Weather", 'detail': "This project aims to solve the short-term prediction of precipitation(rainfall) in 6 hours. Although many meteorologists have provided a reasonably accurate forecast of long-term precipitation, the short-term prediction remains a big challenge. We anticipate an accurate short-term prediction by using artificial intelligence like AlphaGo. In this project, we define useful input data to be utilized for the short-term precipitation and propose machine learning algorithms predicting short-term rainfalls.",  "img": "core/images/project/proj_weather.png"},
            {'title': "Efficient Representation Learning Algorithm for Unlabeled Data", 'detail': "We often unavailable to obtain enough labeled data for our target task(ex. Image Classification) in most real-world cases. Some recent works address the data shortage by proposing un-, semi-, or self- supervised learning methods that utilize unlabeled data to improve the performance in target task without or with only a few amounts of labeled data. In this project, we extend those methods to build a data and training efficient algorithm to cope with various real-world constraints. We start by vision data and then consider sequential data.",  "img": "core/images/project/proj_hynix.png"},
            {'title': "Federated Learning: Development of adaptive lightweight edge linkage analysis technology that enables active immediate response and quick learning", 'detail': "Federated learning (FL) is one of the most popular paradigm of collaborative machine learning. In general, to train the central server (e.g., service manager) in the FL framework, each client (e.g., mobile devices or whole organization) updates its local model via their private data by itself; all local updates are aggregated to the global model; after which the procedure is repeated until convergence. Such FL framework enables us to mitigate many of the systematic privacy risks in the data level, and thus, it has significant potent on the application for the edge computing devices such as phones and tablets. In this project, we aim to analyze the training process of federated learning and optimize the process for better generalization and faster inference.", "img": "core/images/project/proj_etri2.png"},
            {'title': "Designing the ML-based algorithm to analyze semiconductor process data", 'detail': "Even though we can get a wide range of data while developing, producing and testing the semiconductors, it is hard to analyze such unstructured data. However, if we identify the relationship between data and develop a model for them, we can expect to improve its productivity. Since the ML algorithms have shown the promising ability of modeling complex data, this project aims to analyze semiconductor process data utilizing various ML algorithms.", "img": "core/images/project/proj_SDS.jpg"}
        ],

        "project_status": "On-Going Projects"
    }
    return render(request, 'core/projects.html', data)


def past_projects(request):
    data = {
        "menu_active": {
            "projects": "active"
        },

        "project_list": [
            {'title': "Development of XAI-based Technology for Smart Energe Platform", "detail": "This project aims at KEPCO to form a cluster of five schools including KAIST to propose XAI-based smart energy platform technology. In our lab, we study to solve bottlenecks caused by gradient sharing that occurs when training deep learning models with large amounts of data. To solve this problem, we compress the gradient using methods such as Random Projection and Sequential Trasmitting Method.", "img": "core/images/project/proj_kepco.png"},
        ],

        "project_status": "Past Projects"
    }
    return render(request, 'core/projects.html', data)


def conference(request):
    data = {
        "menu_active": {
            "publications": "active"
        }
    }

    return render(request, 'core/conference.html', data)


def journal(request):
    data = {
        "menu_active": {
            "publications": "active"
        }
    }

    return render(request, 'core/journal.html', data)


def patent(request):
    data = {
        "menu_active": {
            "publications": "active"
        }
    }

    return render(request, 'core/patent.html', data)

def seminar(request):
    data = {
        "menu_active": {
            "seminar": "active"
        },
        "this_week_seminar": [],
    }

    path = "/home/osilab/Dropbox/01_Seminar Presentation/1. Seminar_files/Seminar List.xlsx"

    # Sheet name: 'this_week'
    seminar_df = pd.read_excel(path, engine='openpyxl', sheet_name='this_week')
    this_week_seminar_lst = seminar_df.values.tolist()

    for seminar_info in this_week_seminar_lst:
        presenter = seminar_info[0]
        title = seminar_info[2]
        abstract = seminar_info[3]

        if presenter.strip() not in ["", "-"] and title.strip() != "":
            data['this_week_seminar'].append({"presenter": presenter.strip(),
                                              "title": title.strip(),
                                              "abstract": abstract.strip()})

    return render(request, 'core/this_seminar.html', data)


def past_seminar(request):
    data = {
        "menu_active": {
            "seminar": "active"
        },
        "past_seminar_lst": [],
    }

    path = "/home/osilab/Dropbox/01_Seminar Presentation/1. Seminar_files/Seminar List.xlsx"


    # Sheet name:'2020.03~2021.02'
    seminar_df = pd.read_excel(path, engine='openpyxl', sheet_name='2020.03~2021.02')

    seminar_df = seminar_df.replace(np.nan, '', regex=True)

    seminar_lst = seminar_df.values.tolist()

    for _ in range(5):
        seminar_lst.pop(0)

    for seminar_info in seminar_lst:
        presenter = seminar_info[2]
        title = seminar_info[4]

        if presenter.strip() not in ["", "-"] and title.strip() != "":
            data['past_seminar_lst'].append({"presenter": presenter.strip(), "title" : title.strip()})

    return render(request, 'core/past_seminar.html', data)



