import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def driver(request):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    yield driver
    driver.close()


