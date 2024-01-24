import pytest
from selenium.webdriver.common.by import By
from .const import *
from time import sleep


@pytest.mark.parametrize("username, password", users)
def test_login(driver, username, password):
    driver.get(webiste_base_url)
    element_username = driver.find_element(By.NAME, "username")
    element_username.send_keys(username)
    element_password = driver.find_element(By.NAME, "password")
    element_password.send_keys(password)
    submit_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-success")
    submit_button.click()

    sleep(4)