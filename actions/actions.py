# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetWeather(Action):
    def name(self):
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        # Lấy thông tin thành phố từ câu hỏi của người dùng
        city = tracker.get_slot("city")

        if not city:
            dispatcher.utter_message(text="Bạn vui lòng cho tôi biết bạn muốn xem thời tiết ở đâu?")
            return []

        # Gọi API lấy dữ liệu thời tiết
        api_key = "ec75571cea033f0c0e1f1f5c26c51689"  # Thay bằng API key của bạn
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"


        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            message = f"Nhiệt độ hiện tại ở {city} là {temp}°C với thời tiết {weather}."
        else:
            message = "Tôi không tìm thấy thông tin thời tiết cho địa điểm này."

        dispatcher.utter_message(text=message)
        return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

class ActionAskCafe(Action):
    def name(self) -> Text:
        return "action_get_coffee_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # Cấu hình Selenium
            driver_path = r"C:\webdriver\chromedriver-win64\chromedriver.exe"
            service = Service(driver_path)
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Chạy ẩn trình duyệt
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(service=service, options=options)

            # Mở trang web
            url = "https://meoukitchen.sapofnb.vn/"
            driver.get(url)
            time.sleep(5)

            # Lấy và parse HTML
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            parent_div = soup.find("div", id="menu_e2c62a60-b8e7-4383-a080-cea8d3eb1fea")
            
            menu_items = []
            if parent_div:
                name_tags = parent_div.find_all("div", class_="fs-16 ft-w text-breakword mr-b-4 cursor-p")
                menu_items = [tag.text.strip() for tag in name_tags]

            driver.quit()

            if menu_items:
                message = "Menu cafe của Meou Kitchen:\n" + "\n".join(f"☕ {item}" for item in menu_items)
            else:
                message = "Hiện không thể lấy thông tin menu. Bạn vui lòng thử lại sau nhé!"

            dispatcher.utter_message(text=message)

        except Exception as e:
            dispatcher.utter_message(text=f"Có lỗi khi lấy thông tin: {str(e)}")

        return []