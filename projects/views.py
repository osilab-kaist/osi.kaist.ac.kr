from django.shortcuts import render


# Create your views here.
def ongoing_projects(request):
    data = {
        "menu_active": {
            "projects": "active"
        },

        "project_list": [
            {'title': "AutoML", "detail": "The neural architecture search (NAS) has been a great success in a variety of applications such as image classification and natural language processing. Despite huge success, it faces a challenge that takes too much resource budgets (e.g.,  computational costs and storage), which stems from the vastness of NAS's search space. In this project, we aim to reduce the tremendous resource budget required due to the large search space.", "img": "images/project/proj_etri.png"},
            {'title': "Developing Models for Predicting Properties of Compounds using Artificial Neural Network", 'detail': "Properties of tire compounds are closely related to the performance of tire. Therefore, one of the goals of this project is to develop models to predict properties of the compounds. Moreover, we aim to develop inverse design models to suggest proper compounds for the target properties. We also propose automatic systems for building AI models.",  "img": "images/project/proj_hankooktire.png"},
            {'title': "Explainable intelligent system for optimal strategy in battles", 'detail': "Recently, artificial neural networks have shown remarkable successes with huge datasets. However, with scarce data, artificial neural networks are terrible.  In military situations, unfortunately, it is difficult to obtain a large training dataset.  Military cases also require to explain the decisions that the algorithm generates, which is very tricky with general artificial neural networks. In this project, we address these problems and design new approaches using Bayesian frameworks.",  "img": "images/project/proj_add.png"},
            {'title': "Alpha Weather", 'detail': "This project aims to solve the short-term prediction of precipitation(rainfall) in 6 hours. Although many meteorologists have provided a reasonably accurate forecast of long-term precipitation, the short-term prediction remains a big challenge. We anticipate an accurate short-term prediction by using artificial intelligence like AlphaGo. In this project, we define useful input data to be utilized for the short-term precipitation and propose machine learning algorithms predicting short-term rainfalls.",  "img": "images/project/proj_weather.png"},
            {'title': "Efficient Representation Learning Algorithm for Unlabeled Data", 'detail': "We often unavailable to obtain enough labeled data for our target task(ex. Image Classification) in most real-world cases. Some recent works address the data shortage by proposing un-, semi-, or self- supervised learning methods that utilize unlabeled data to improve the performance in target task without or with only a few amounts of labeled data. In this project, we extend those methods to build a data and training efficient algorithm to cope with various real-world constraints. We start by vision data and then consider sequential data.",  "img": "images/project/proj_hynix.png"},
            {'title': "Federated Learning: Development of adaptive lightweight edge linkage analysis technology that enables active immediate response and quick learning", 'detail': "Federated learning (FL) is one of the most popular paradigm of collaborative machine learning. In general, to train the central server (e.g., service manager) in the FL framework, each client (e.g., mobile devices or whole organization) updates its local model via their private data by itself; all local updates are aggregated to the global model; after which the procedure is repeated until convergence. Such FL framework enables us to mitigate many of the systematic privacy risks in the data level, and thus, it has significant potent on the application for the edge computing devices such as phones and tablets. In this project, we aim to analyze the training process of federated learning and optimize the process for better generalization and faster inference.", "img": "images/project/proj_etri2.png"},
            {'title': "Designing the ML-based algorithm to analyze semiconductor process data", 'detail': "Even though we can get a wide range of data while developing, producing and testing the semiconductors, it is hard to analyze such unstructured data. However, if we identify the relationship between data and develop a model for them, we can expect to improve its productivity. Since the ML algorithms have shown the promising ability of modeling complex data, this project aims to analyze semiconductor process data utilizing various ML algorithms.", "img": "images/project/proj_SDS.jpg"}
        ],

        "project_status": "On-Going Projects"
    }
    return render(request, 'projects.html', data)


def past_projects(request):
    data = {
        "menu_active": {
            "projects": "active"
        },

        "project_list": [
            {'title': "Development of XAI-based Technology for Smart Energe Platform", "detail": "This project aims at KEPCO to form a cluster of five schools including KAIST to propose XAI-based smart energy platform technology. In our lab, we study to solve bottlenecks caused by gradient sharing that occurs when training deep learning models with large amounts of data. To solve this problem, we compress the gradient using methods such as Random Projection and Sequential Trasmitting Method.", "img": "images/project/proj_kepco.png"},
        ],

        "project_status": "Past Projects"
    }
    return render(request, 'projects.html', data)


