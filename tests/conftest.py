import pytest
import subprocess
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


@pytest.fixture(scope="function")
def driver(request):
    chrome_driver_path = ChromeDriverManager().install()
    chrome_service = webdriver.chrome.service.Service(chrome_driver_path)
    driver = webdriver.Chrome(service=chrome_service)
    yield driver
    driver.close()


@pytest.fixture(scope="session", autouse=True)
def run_server():
    manage_py_file_path = os.path.join("src", "manage.py")
    server_process = subprocess.Popen(["python3", manage_py_file_path, "runserver"])
    sleep(2)
    yield server_process
    server_process.terminate()
    server_process.wait(timeout=2)
