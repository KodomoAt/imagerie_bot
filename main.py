import requests
import json
import datetime
import locale
from send_email import send_email
import os

# Définition de la langue locale à utiliser
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

url = os.getenv("IMAGERIE_URL")

payload = json.dumps({
  "examTypeId": "1998",
  "minDate": "20230422",
  "examId": "30232",
  "examSetId": None,
  "practitionerId": None,
  "onlyMasterOffice": False,
  "officePlaceIds": None,
  "referrer": ""
})
headers = {
  'Content-Type': 'application/json',
  'Cookie': os.getenv('COOKIE')
}

response = requests.request("POST", url, headers=headers, data=payload)
next_appointment = []
for day in response.json()["availabilityLines"]:
    for appointment in day["appointments"]:
        if appointment != None:
            next_appointment.append(datetime.datetime.strptime(appointment['start'], "%Y-%m-%dT%H:%M:%S"))

result = list(map(lambda x: x.strftime("%A %d %B %Y à %H:%M:%S"),list(filter(lambda x: x < datetime.datetime(2023, 5, 26, 0, 0, 0), next_appointment))))
print(result)



if result : 
    send_email(os.getenv("RECEIVER"), result)


    