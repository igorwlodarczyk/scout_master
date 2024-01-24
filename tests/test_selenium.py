import pytest


def test_open_page(driver):
    driver.get("http://127.0.0.1:8000")