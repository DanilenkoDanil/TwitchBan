from selenium import webdriver
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as es
from selenium.common.exceptions import TimeoutException


def is_channel_banned(channel_name):
    url = f"https://www.twitch.tv/{channel_name}"
    driver = webdriver.Chrome()  # Change this to the path of your webdriver executable
    driver.get(url)
    try:
        WebDriverWait(driver, timeout=3).until(es.presence_of_element_located((By.XPATH, "//*[contains(text(), 'В данный момент этот канал недоступен из-за нарушения Правил сообщества или Условий продаж Twitch.')]")))
        return True
    except TimeoutException:
        return False


print(is_channel_banned('just_ns'))
