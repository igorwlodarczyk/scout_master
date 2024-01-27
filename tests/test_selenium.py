import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .const import *

login_dependency = pytest.mark.dependency(
    depends=[f"test_login[{user}-{password}]" for user, password in users]
)


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


@login_dependency
def test_placeholder():
    ...


@login_dependency
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@pytest.mark.parametrize(
    "player_name, player_club",
    [("Lautaro Martinez", "Inter"), ("Kylian Mbappe", "Paris SG")],
)
@pytest.mark.parametrize("rating, minutes_played", [(8.4, 90), (6.3, 18)])
def test_scout_report_create_delete(
    driver, player_name, player_club, rating, minutes_played
):
    """
    Test creates a scout report, verifies its creation, and then deletes the report
    to ensure successful creation and deletion.

    Args:
        driver (WebDriver): Selenium WebDriver instance.
        player_name (str): Name of the player for the scout report.
        player_club (str): Club of the player for the scout report.
        rating (float): Rating of the player for the scout report.
        minutes_played (int): Minutes played by the player for the scout report.

    Returns:
        None
    """
    username, password = users[0]
    wait = WebDriverWait(driver, 10)
    driver.get(website_base_url)
    login_procedure(driver, username, password)

    create_report_element = driver.find_element(By.XPATH, "//a[text()='Create report']")
    create_report_element.click()

    player_select_element = driver.find_element(By.NAME, "player")
    player_select = Select(player_select_element)
    player_select.select_by_visible_text(f"{player_name} - {player_club}")

    match_select_element = driver.find_element(By.NAME, "match")
    match_select = Select(match_select_element)
    match_options = list(
        filter(
            lambda option: player_club in option,
            [option.text for option in match_select.options],
        )
    )
    match_select.select_by_visible_text(match_options[0])

    rating_element = driver.find_element(By.NAME, "rating")
    rating_element.send_keys(rating)

    minutes_element = driver.find_element(By.NAME, "minutes_played")
    minutes_element.send_keys(minutes_played)

    submit_button = driver.find_element(By.CSS_SELECTOR, "input.input_button")
    submit_button.click()

    success_element = driver.find_element(By.XPATH, "//p[text()='Success!']")
    assert driver.current_url == website_base_url + "success"
    assert success_element

    home_page_element = driver.find_element(By.XPATH, "//a[text()='Return to home']")
    home_page_element.click()

    view_reports_element = driver.find_element(By.XPATH, "//a[text()='View reports']")
    view_reports_element.click()

    player_rows = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//table[@class='content_table']//tr")
        )
    )
    player_row = player_rows[1]
    player_row_text = player_row.text

    assert player_name in player_row_text
    assert player_club in player_row_text
    assert str(minutes_played) in player_row_text
    assert str(rating) in player_row_text

    delete_button = player_row.find_element(By.XPATH, ".//button[text()='Delete']")
    delete_button.click()

    assert driver.current_url == website_base_url + "view-reports"
    player_rows = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//table[@class='content_table']//tr")
        )
    )
    assert player_row_text != player_rows[1].text
