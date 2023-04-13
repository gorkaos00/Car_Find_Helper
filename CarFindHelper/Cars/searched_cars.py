import requests
from bs4 import BeautifulSoup as bs
import re
import csv
from pathlib import Path
from typing import List
import os



def element_exists(lst, element):
    try:
        lst.index(element)
        return True
    except ValueError:
        return False


def index_of_column_header(column_header: str) -> int:
    """"""
    with open("migrations/Cars5.csv", 'r') as file:
        header = file.readline()
    return header.split(',').index(column_header)


def read_csv_file(input_file: str) -> List[List[str]]:
    # list comprehension
    return [row for row in csv.reader(Path(input_file).read_text(encoding="utf-8").splitlines(), delimiter=',')]


def merge(list1, list2, list3, list4):
    merged_list = list(zip(list1, list2, list3, list4))
    return merged_list


def compare_cars(eco, power, drive, type, min_price, max_price, age_min, age_max):
    working = 1
    if 50 < eco <= 75:  ##Changing economic value to capacity of engine
        eco = 2000.0
    elif 75 < eco <= 100:
        eco = 1500.0
    elif 25 < eco <= 50:
        eco = 3000.0
    else:
        eco = 8000.0

    if 25 < power <= 50:  ##Changing power value to horsepower of car
        power = 150.0
    elif 50 < power <= 75:
        power = 200
    elif 75 < eco <= 100:
        power = 250
    else:
        power = 0

    data = read_csv_file("Cars5.csv")[0:]  ## Reading data from csv file
    cars_from_csv = list(map(lambda el: (str(el[1]).lower(), str(el[2]).lower(), int(el[3]), float(el[0])),
                             filter(lambda el: (
                                     str(el[4]).find(drive) != -1 and str(el[5]) == type and min_price <= float(
                                 el[0]) <= max_price and age_max >= int(
                                 el[3]) >= age_min and float(el[6]) < eco and power < float(el[7])), data)))

    ##Sorting and deleting reapeted lines
    cars_from_csv = list(dict.fromkeys(cars_from_csv))
    cars_from_csv = list(map(list, cars_from_csv))

    for car in cars_from_csv:
        for car_generation in cars_from_csv:
            if car[0] == car_generation[0] and car[1] == car_generation[1] and car[2] == car_generation[2]:
                car[3] = car_generation[3]
    cars_from_csv = list(map(tuple, cars_from_csv))
    cars_from_csv = list(dict.fromkeys(cars_from_csv))
    cars_from_csv = list(map(list, cars_from_csv))

    data = {}
    car_rate = []
    car_image = []
    car_name = []
    car_price = []
    generation_sides = []
    print (cars_from_csv)
    for car in cars_from_csv:
        ##Checking if site exist
        car_side = requests.head("https://motofakty.pl/samochody/opinie/" + car[0] + "/" + car[1] + "/")
        print(car[0]+car[1])
        if car_side.status_code != 200:
            print("Brak strony")
        else:
            # Taking Generation of each model to compare it to a given age
            car_side = requests.get("https://motofakty.pl/samochody/opinie/" + car[0] + "/" + car[1] + "/")
            car_soup = bs(car_side.content, 'html.parser')
            car_class = car_soup.find('section', attrs={'class': 'listaGeneracji hreview-aggregate'})
            generation = []
            generation = car_class.findAll('a')

            for car_generation in generation:
                car_generation = str(car_generation['href'])
                if (
                        car_generation[
                        -4:]) != 'html':  # on this side when generation is not create site url ends with html
                    car_side = requests.get("https://motofakty.pl" + car_generation)
                    if (car_generation[-6:-1]) == 'teraz':  # when the generation of a car is still produced
                        generation_production_min_age = int(car_generation[-11:-7])
                        generation_production_max_age = 2023
                    elif str(car_generation[
                             -5:-1]).isdigit():  # when generation of a car ends this string should be digit
                        generation_production_max_age = int(car_generation[-5:-1])
                        generation_production_min_age = int(car_generation[-10:-6])
                    else:
                        generation_production_min_age = 1
                        generation_production_max_age = 0
                    if generation_production_min_age < age_max - 1 < generation_production_max_age:  # checking if given age compare to production time of generation
                        if (element_exists(generation_sides, car_generation)) == False:
                            # Taking all requested things
                            generation_sides.append(car_generation)
                            car_side = requests.get("https://motofakty.pl" + car_generation)
                            car_soup = bs(car_side.content, 'html.parser')
                            car_site = car_soup.find('article', attrs={'class': 'hreview-aggregate'})
                            temp_img = car_site.find('div', attrs={'class': 'zdjecie'})
                            temp_rate = car_soup.find('span', attrs={'class': 'average'})

                            car[0] = car[0].replace("-", " ")
                            car[1] = car[1].replace("-", " ")
                            car[0] = car[0].title()  # Making car names
                            car[1] = car[1].title()
                            car_name.append(" " + car[0] + " " + car[1])
                            temp_rate = re.findall("\d+\,\d+", str(temp_rate))

                            temp_rate = str(temp_rate)  # making car rate
                            temp_rate = temp_rate.replace(",", ".")
                            temp_rate = float(temp_rate[2:6])
                            car_rate.append("Ocena:\n" + str(temp_rate) + "/5.0")

                            temp_img = str(temp_img)  # making car img
                            temp_img = re.search("url\(\'(.+?)\'\)", temp_img)
                            temp_img = temp_img.group(1)
                            car_image.append(temp_img)
                            car_price.append("Srednia Cena:\n" + str(car[3]) + " zl")  # and car price
    Cars = []
    if working == 1:
        Cars = merge(car_rate, car_image, car_name, car_price)
        Cars.sort(reverse=True)  # sorting by ratings
        if len(Cars) > 8:
            Cars = Cars[0:8]
        elif 4 < len(Cars) <= 8:
            Cars = Cars[0:4]
    data.update({
        "Cars": Cars,
        "ilosc": len(car_rate),
        "working": working
    })
    print(data)
    return data
