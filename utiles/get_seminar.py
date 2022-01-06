import pandas as pd
import numpy as np

path = "/home/osilab/Dropbox/OSI LAB/01_Seminar Presentation/1. Seminar_files/Seminar List.xlsx"


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
        print(presenter, title)

