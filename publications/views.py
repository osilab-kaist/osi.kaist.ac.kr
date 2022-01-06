from django.shortcuts import render


# Create your views here.
def conference(request):
    data = {
        "menu_active": {
            "publications": "active"
        }
    }

    return render(request, 'conference.html', data)


def journal(request):
    data = {
        "menu_active": {
            "publications": "active"
        }
    }

    return render(request, 'journal.html', data)


def patent(request):
    data = {
        "menu_active": {
            "publications": "active"
        }
    }

    return render(request, 'patent.html', data)
