import time  # pip3 install time
import requests  # pip3 install requests
import numpy as np  # pip3 install numpy
from random import Random
from threading import Thread

import urllib3  # pip3 install urllib3


# # Đường dẫn đến file mô hình
# model_path = 'my_model.h5'

# Tải mô hình
#model = load_model(model_path)

def get_token(username, password):
    session = requests.Session()
    session.auth = (username, password)
    session.verify = False
    session.headers.update({"Content-Type": "application/x-www-form-urlencoded"})

    try:
        response = session.post(
            "https://104.43.95.53/auth/realms/master/protocol/openid-connect/token",
            
            data={"grant_type": "client_credentials", "client_id": "uiot"},
        )
    except requests.exceptions.RequestException as e:
        print(f"(0) Request failed with error: {e}")
        return None
   
    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        print(f"(0) Request failed with status code: {response.status_code}")
        return None
    

def get_data(token):
    session = requests.Session()
    session.verify = False
    session.headers.update(
        {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
 
    response = session.get("https://104.43.95.53/api/master/asset/6SSoa1kKCa6f9L27XNH0P9")
   
    if response.status_code == 200:
        data = response.json()
        return parse_data(data)
    else:
        print(f"(1) Request failed with status code: {response.status_code}")
        return None



def parse_data(data):
    attributes = data.get("attributes")
    
    if attributes:
        # Trích xuất giá trị của PM25, CO2 và PM10 từ thuộc tính
        PM25_value = attributes.get("PM25", {}).get("value")
        CO2_value = attributes.get("CO2", {}).get("value")
        PM10_value = attributes.get("PM10", {}).get("value")
        
        # Kiểm tra xem tất cả các giá trị đã được trích xuất thành công không
        if PM25_value is not None and CO2_value is not None and PM10_value is not None:
            # Tạo một mảng numpy chứa các giá trị PM25, CO2 và PM10
            data_array = np.array([[CO2_value, PM10_value, PM25_value]])
            print(data_array)
            return data_array
        else:
            print("Some PM25, CO2, or PM10 values are missing or invalid.")
            return None
    else:
        print("No attributes found in data.")
        return None
    
def main():

    token1 = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI1cGwtMWdBMHEwV1REU0xqMU01ckdnWDBBbWxETHVZb0xMeG1ILUUwZFNVIn0.eyJleHAiOjE3MTUwMjY4ODUsImlhdCI6MTcxNDk2Njg4NSwiYXV0aF90aW1lIjoxNzE0OTY0MTI2LCJqdGkiOiI0M2NjOWI2OS1iY2JjLTRiZTctOTNhNi1mOTdmM2M2MjE2YzUiLCJpc3MiOiJodHRwczovLzEwNC40My45NS41My9hdXRoL3JlYWxtcy9tYXN0ZXIiLCJhdWQiOlsibWFzdGVyLXJlYWxtIiwiYWNjb3VudCJdLCJzdWIiOiJhYmE4YjhkMy0yY2E3LTQ3OGYtOGJjMy0wMzc1YWJhZDFlYzQiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJvcGVucmVtb3RlIiwic2Vzc2lvbl9zdGF0ZSI6ImEyNTI2Yjk0LTYzOTgtNDgwYy1iNmE4LWRiZWQ5MTQ3MTU1ZCIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly8xMDQuNDMuOTUuNTMiLCJodHRwczovL3Rlc3QubG9jYWwiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImNyZWF0ZS1yZWFsbSIsImRlZmF1bHQtcm9sZXMtbWFzdGVyIiwib2ZmbGluZV9hY2Nlc3MiLCJhZG1pbiIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsib3BlbnJlbW90ZSI6eyJyb2xlcyI6WyJ3cml0ZTpsb2dzIiwid3JpdGU6YXNzZXRzIiwicmVhZCIsIndyaXRlOmFkbWluIiwicmVhZDpsb2dzIiwicmVhZDptYXAiLCJyZWFkOmFzc2V0cyIsIndyaXRlOnVzZXIiLCJyZWFkOnVzZXJzIiwid3JpdGU6cnVsZXMiLCJyZWFkOnJ1bGVzIiwicmVhZDppbnNpZ2h0cyIsIndyaXRlOmF0dHJpYnV0ZXMiLCJ3cml0ZSIsIndyaXRlOmluc2lnaHRzIiwicmVhZDphZG1pbiJdfSwibWFzdGVyLXJlYWxtIjp7InJvbGVzIjpbInZpZXctcmVhbG0iLCJ2aWV3LWlkZW50aXR5LXByb3ZpZGVycyIsIm1hbmFnZS1pZGVudGl0eS1wcm92aWRlcnMiLCJpbXBlcnNvbmF0aW9uIiwiY3JlYXRlLWNsaWVudCIsIm1hbmFnZS11c2VycyIsInF1ZXJ5LXJlYWxtcyIsInZpZXctYXV0aG9yaXphdGlvbiIsInF1ZXJ5LWNsaWVudHMiLCJxdWVyeS11c2VycyIsIm1hbmFnZS1ldmVudHMiLCJtYW5hZ2UtcmVhbG0iLCJ2aWV3LWV2ZW50cyIsInZpZXctdXNlcnMiLCJ2aWV3LWNsaWVudHMiLCJtYW5hZ2UtYXV0aG9yaXphdGlvbiIsIm1hbmFnZS1jbGllbnRzIiwicXVlcnktZ3JvdXBzIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwic2lkIjoiYTI1MjZiOTQtNjM5OC00ODBjLWI2YTgtZGJlZDkxNDcxNTVkIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiU3lzdGVtIEFkbWluaXN0cmF0b3IiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbiIsImdpdmVuX25hbWUiOiJTeXN0ZW0iLCJmYW1pbHlfbmFtZSI6IkFkbWluaXN0cmF0b3IifQ.T837s99U1HobrXhBr_J0jX1J8-nyFNXUAuAtS5-oUWbT3rhdfuCcORM4DOtn4AH9PxtdMIYeBgXPhCnFGih-Jx_zU4vKE2Tehd26JWTWG3K7LDtr4Jvlo0JHiprgc4EPx2TzZVIYGrc6eYV9m9nGk72NqD5EIFT9Dp4eDBCmSuTiopFeNpUM7m3tnlsJZon210QK8M9uFfx6-CHae3kjl8LjQ6goh7Js5LWZBPkYps1fNJB8XGJpCm7UR3O7HI6ohwp251gDw1DqC741OB_2ZE8jXt1vJ98uQxURJrycT87uPAr8PiCUNPSLw5W3D2N5btN42d85Xp08u0pqRhtALA"
    username = "uiot"
    password = "qCKn5z1iZAkU86N2fH9lkRiL9GIk53CX"
    while True:
        print("Predicting...")

        token = get_token(username, password)

        if not token:
            print("Failed to get token")
            time.sleep(10)
            continue
        # else:
        #     print(token)
        get_data(token1)
        # result = predict(get_data(token))
        # print(result)
        # put_data(token, result)

        time.sleep(10)  # 5 minutes


if __name__ == "__main__":
    main()