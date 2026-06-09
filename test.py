import easyocr
import pandas as pd
from datetime import datetime

reader = easyocr.Reader(['en'])

result = reader.readtext('images/car.jpg')

vehicle_no = ""

for item in result:
    text = item[1]

    if "JK" in text.upper():
        vehicle_no = text.upper()
        vehicle_no = vehicle_no.replace("Z", "7")
        break

print("Vehicle Number:", vehicle_no)

data = {
    "Vehicle_Number": [vehicle_no],
    "Date": [datetime.now().strftime("%Y-%m-%d")],
    "Time": [datetime.now().strftime("%H:%M:%S")]
}

df = pd.DataFrame(data)
df.to_csv("vehicles.csv", mode="a", header=False, index=False)

print("Saved to vehicles.csv")