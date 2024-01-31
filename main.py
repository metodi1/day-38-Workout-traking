from datetime import datetime

import requests
import os

API_KEY = os.environ["API_KEY"]
APP_ID = os.environ['APP_ID']
GOOGLE_SHEET_NAME = os.environ['GOOGLE_SHEET_NAME']
sheety_authentication = os.environ['sheety_authentication']
sheety_end_point = os.environ['sheety_end_point']

GENDER = "male"
WEIGHT_KG = 82
HEIGHT_CM = 186
AGE = 41

# -----------------------------------nutritionix---------------------------#

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercises you did: ")

headers = {
    'Content-Type': 'application/json',
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

respond = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = respond.json()

# -----------------------------------Sheety---------------------------#

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
for exercise in result["exercises"]:
    sheet_inputs = {
        GOOGLE_SHEET_NAME: {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

# Sheety Authentication Option 3: Bearer Token

bearer_headers = {
    "Authorization": f"{sheety_authentication}"
}
sheet_response = requests.post(
    sheety_end_point,
    json=sheet_inputs,
    headers=bearer_headers
)

print(f"Sheety Response: \n {sheet_response.json()}")
