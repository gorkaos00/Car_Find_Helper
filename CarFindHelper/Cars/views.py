from django.shortcuts import render
from Cars import searched_cars

def about(request):
    return render(request,"about.html")


def index(request):
    if request.method == 'POST':
        min_price = request.POST.get("min_price")
        max_price = request.POST.get("max_price")
        type = request.POST.get("Type")
        drive = request.POST.get("drive")
        eco = int(request.POST.get("eco"))
        age_min = request.POST.get("age_min")
        age_max = request.POST.get("age_max")
        power = int(request.POST.get("power"))
        if min_price == "":
            min_price = 0
        if max_price == "":
            max_price = 1000000
        if age_min == "":
            age_min = 1900
        if age_max == "":
            age_max = 2023
        if type == None:
            type = "sedan"
        if drive == None:
            drive = "Front wheels"
        working = 1
        type = str(type)
        drive = str(drive)
        age_min = int(age_min)
        age_max = int(age_max)
        min_price = float(min_price)
        max_price = float(max_price)
        data=searched_cars.compare_cars(eco,power,drive,type,min_price,max_price,age_min,age_max)
        return render(request,"result.html",data)
    else:
        data={}
        return render(request, "index.html", data)
