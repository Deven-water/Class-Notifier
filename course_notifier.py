import time
import requests
from bs4 import BeautifulSoup

from webhook import WEBHOOK

CLASS_DETAILS_URL = "" \
"https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/getClassDetails"
ENROLL_INFO_URL = "" \
"https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/getEnrollmentInfo"

FREQUENCY = 60
SEATS_AVAILABLE = "Enrollment Seats Available:"
CLASSES = [10061, 10473]

def crn_converter(term: int, crns: list[int]) -> list[str]:
    """find the name for the CRN"""

    class_names = []

    for crn in crns:
        data = requests.post(CLASS_DETAILS_URL, params ={
            "term": term,
            "courseReferenceNumber": crn
            }, timeout=5)

        soup = BeautifulSoup(data.text, "html.parser")

        class_info = soup.find_all("span")
        class_info_dict = {}

        for heading, info in zip(class_info[::2], class_info[1::2]):
            class_info_dict[heading.text] = info.text

        class_names.append(f"{class_info_dict["Subject:"]} {class_info_dict["Course Number:"]}")

    return class_names


def notifier(term: int, crns: list[int], names_classes: list[str]) -> None:
    """notifier for classes"""
    for i, crn in enumerate(crns):
        data = requests.post(ENROLL_INFO_URL, params ={
        "term": term,
        "courseReferenceNumber": crn
        }, timeout=5)

        soup = BeautifulSoup(data.text, "html.parser")

        enroll_info = soup.find_all("span")
        enroll_info_dict = {}

        for heading, info in zip(enroll_info[::2], enroll_info[1::2]):
            enroll_info_dict[heading.text] = int(info.text)

        if enroll_info_dict[SEATS_AVAILABLE] > 0:
            requests.post(WEBHOOK, json={
                "content": 
                f'@everyone SEAT(S) AVAILABLE! {names_classes[i]} has {enroll_info_dict[SEATS_AVAILABLE]} seat(s).'},
                timeout=5)
        else:
            requests.post(WEBHOOK, json={
                "content": 
                f'NO SEATS AVAILABLE. {names_classes[i]} has {enroll_info_dict[SEATS_AVAILABLE]} seat(s).'},
                timeout=5)

names = crn_converter(202710, CLASSES)

while True:
    notifier(202710, CLASSES, names)
    time.sleep(FREQUENCY)
