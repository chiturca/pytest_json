import pytest
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSauceDemo:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")

    def teardown_method(self):
        self.driver.quit()

    def login(self, username, password):
        username_input = self.driver.find_element(By.ID, "user-name")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")
        
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        login_button.click()

    
    #Eski ödevdeki;
        # -Kullanıcı adı ve şifre alanları boş geçildiğinde uyarı mesajı olarak "Epic sadface: Username is required" gösterilmelidir.
        # -Sadece şifre alanı boş geçildiğinde uyarı mesajı olarak "Epic sadface: Password is required" gösterilmelidir.
        # -Kullanıcı adı "locked_out_user" şifre alanı "secret_sauce" gönderildiğinde "Epic sadface: Sorry, this user has been locked out." mesajı gösterilmelidir.
    #kısımlarını tek fonksiyonda birleştirip parametrize'ı json ile birlikte buradaki hatalı girişler için kullandım.
    def read_test_data():
        with open("test_data.json", "r") as file:
            data = json.load(file)
        return [(item["username"], item["password"], item["expected_error"]) for item in data["login_cases"]]

    @pytest.mark.parametrize("username, password, expected_error", read_test_data())
    def test_login_errors(self, username, password, expected_error):
        self.login(username, password)
        error_message = self.driver.find_element(By.CSS_SELECTOR, "#login_button_container > div > form > div.error-message-container.error")
        assert error_message.text == expected_error