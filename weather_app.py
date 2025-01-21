# This is to try and make a UI based weather app to improve my understanding of APIs and PyQt5

# imports
import sys
import requests
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QSizePolicy)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget): #class WeatherApp inherits from the parent class QWidget
      def __init__(self):
            super().__init__()
            self.city_label = QLabel("Enter city name: ", self)
            self.city_input = QLineEdit(self)
            self.get_weather_button = QPushButton("Get weather",self)
            self.temperature_label = QLabel(self)
            self.emoji_label = QLabel(self)
            self.description_label = QLabel(self)
            self.initUI()

      def initUI(self):
            self.setWindowTitle("Weather App")
            
            vbox = QVBoxLayout()
            vbox.addWidget(self.city_label)
            vbox.addWidget(self.city_input, stretch = 1)
            vbox.addWidget(self.get_weather_button)
            vbox.addWidget(self.temperature_label)
            vbox.addWidget(self.emoji_label)
            vbox.addWidget(self.description_label)

            self.setLayout(vbox)
            #self.city_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.city_input.setFixedHeight(60)

            self.city_label.setAlignment(Qt.AlignCenter)
            self.city_input.setAlignment(Qt.AlignCenter)
            self.temperature_label.setAlignment(Qt.AlignCenter)
            self.emoji_label.setAlignment(Qt.AlignCenter)
            self.description_label.setAlignment(Qt.AlignCenter)

            self.city_label.setObjectName("city_label")
            self.city_input.setObjectName("city_input")
            self.get_weather_button.setObjectName("get_weather_button")
            self.temperature_label.setObjectName("temperature_label")
            self.emoji_label.setObjectName("emoji_label")
            self.description_label.setObjectName("description_label")

            self.setStyleSheet("""
                  QLabel, QPushButton{
                        font-family: calibri;
                  }
                  QLabel#city_label{
                        font-size: 40px;
                        font-style: italic;
                  }
                  QLineEdit#city_input{
                        font-size: 40px;
                  }
                  QPushButton#get_weather_button{
                        font-size: 30px;
                        font-weight: bold;
                  }
                  QLabel#temperature_label{
                        font-size: 75px;
                  }
                  QLabel#emoji_label{
                        font-size: 100px;
                        font-family: Apple Color Emoji; 
                  }
                  QLabel#description_label{
                        font-size: 50px;       
                  }
            """)

            self.get_weather_button.clicked.connect(self.get_weather)
            

      def get_weather(self):
            
            api_key = "850b6b7e5c41b9d47b17bc1040fe79e7"
            city = self.city_input.text()
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

            try:
                  response = requests.get(url)
                  response.raise_for_status()
                  data = response.json()

                  if data["cod"] == 200:
                        self.display_weather(data)
            
            except requests.exceptions.HTTPError as http_error:
                  match response.status_code:
                        case 400:
                              self.display_error("Bad request:\nPlease check your input")
                        case 401:
                              self.display_error("Unauthorized:\nInvalid API key")
                        case 403:
                              self.display_error("Forbidden:\nAccess Denied")
                        case 404:
                              self.display_error("Not found:\nCity not found")
                        case 500:
                              self.display_error("Internal Server Error:\nPlease try again later")
                        case 502:
                              self.display_error("Bad Gateway:\nInvalid response from the server")
                        case 503:
                              self.display_error("Service Unavailable:\nServer is down")
                        case 504:
                              self.display_error("Gatewat Timeout:\nNo resposne from the server")
                        case _:
                              self.display_error(f"HTTP error occured:\n{http_error}")
            except requests.exceptions.ConnectionError:
                  self.display_error("Connection Error:\n Check your internet connection")
            except requests.exceptions.Timeout:
                  self.display_error("Timeout Error:\nThe request timed out")
            except requests.exceptions.TooManyRedirects:
                  self.display_error("Too many Redirects:\nCheck the URL")
            except requests.exceptions.RequestException as req_error:
                  self.display_error(f"Request Error:\n{req_error}")
            
      
      def display_error(self, message):
            self.temperature_label.setStyleSheet("font-size: 30px;")
            self.temperature_label.setText(message)

      def display_weather(self, data):
            self.temperature_label.setStyleSheet("font-size: 75px;")
            temperature_k = data["main"]["temp"]
            temperature_c = temperature_k - 273.15
            #temperature_f = (temperature_k * 9/5) - 459.67
            weather_id = data["weather"][0]["id"]
            weather_description = data["weather"][0]["description"]

            self.temperature_label.setText(f"{temperature_c:.0f}°C")
            self.emoji_label.setText(self.get_weather_emoji(weather_id))
            self.description_label.setText(weather_description)

      @staticmethod
      def get_weather_emoji(weather_id):
            match weather_id:
                        case _ if 200 <= weather_id <= 232:
                              return "⚡"
                        case _ if 300 <= weather_id <= 321:
                              return "🌦️"
                        case _ if 500 <= weather_id <= 531:
                              return "🌧️"
                        case _ if 600 <= weather_id <= 622:
                              return "❄️"
                        case _ if 701 <= weather_id <= 741:
                              return "🌫️"
                        case _ if weather_id == 762:
                              return "🌋"
                        case _ if weather_id == 771:
                              return "💨"
                        case _ if weather_id == 781:
                              return "🌪️"
                        case _ if weather_id == 800:
                              return "☀️"
                        case _ if 801 <= weather_id <= 804:
                              return "☁️"
                        case _:
                              return""
                       

      
if __name__ == "__main__":
      app = QApplication(sys.argv)
      weather_app = WeatherApp() # constructed the weather_app object
      weather_app.show()         # showing the object
      sys.exit(app.exec_())
