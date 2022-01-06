from django.shortcuts import render
from os import listdir
from os.path import isfile, join

# Create your views here.
def photo(request):
    main_path = "/home/osilab4/homepage/osilab_homepage/static/images/photo/"

    photo_data = {
        # '2019': ["2017_1.jpeg", "2017_2.jpeg", "2017_3.jpeg", "2017_4.jpeg", "2018_1.jpeg", "2018_2.jpeg",
        #          '2019_1.jpg', '2019_2.jpg'],
        # '2020': ["2020_1.jpg", "2020_2.jpg", "2020_3.jpg", "2020_4.jpg", "2020_5.jpg", "2020_6.jpg", "2020_7.jpg",
        #          "2020_8.jpg", "2020_9.jpg", "2020_10.jpg", "2020_11.jpg", ],
        '2019': [f for f in listdir(main_path + "2019") if isfile(join(main_path + "2019", f))],
        '2020': [f for f in listdir(main_path + "2020") if isfile(join(main_path + "2020", f))],
        '2021': [f for f in listdir(main_path + "2021") if isfile(join(main_path + "2021", f))]
    }

    data = {
        "menu_active": {
            "photo": "active"
        },
    }

    path_info = request.path_info
    year = path_info.split("/")[-1]

    data['photo_lst'] = photo_data[year]
    data['year'] = year

    return render(request, 'photo.html', data)
