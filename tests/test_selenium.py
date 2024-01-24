import pytest
from selenium.webdriver.common.by import By
from .const import *
from time import sleep


def login_procedure(driver, username, password):
    element_username = driver.find_element(By.NAME, "username")
    element_username.send_keys(username)
    element_password = driver.find_element(By.NAME, "password")
    element_password.send_keys(password)
    submit_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-success")
    submit_button.click()


@pytest.mark.dependency()
@pytest.mark.parametrize("username, password", users)
def test_login(driver, username, password):
    driver.get(website_base_url)
    login_procedure(driver, username, password)
    assert driver.current_url == website_base_url


@pytest.mark.dependency(
    depends=[f"test_login[{user}-{password}]" for user, password in users]
)
def test_placeholder():
    ...
