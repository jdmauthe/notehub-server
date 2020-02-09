import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notehub_project.settings")

import django

django.setup()

from api.models import University

csv_name = "uni.csv"


def add_data(name):
    d, created = University.objects.get_or_create(name=name)
    # print("- Data: {0}, Created: {1}".format(str(name), str(created)))
    return created


def populate():
    # data is a list of lists
    with open(csv_name, "r") as csv_file:
        reader = csv.reader(csv_file)
        for name in reader:
            add_data(name[0])


if __name__ == "__main__":
    print("Starting population of universities")
    populate()
    print("Population of universities done")
