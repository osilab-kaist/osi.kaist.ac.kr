from django.shortcuts import render
import pandas as pd
import numpy as np


# Create your views here.
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

    return render(request, 'this_seminar.html', data)


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

    return render(request, 'past_seminar.html', data)

