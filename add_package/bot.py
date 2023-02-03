from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from re import search
import time
import getpass


def add_route_details(data: list, route: list):
    driver = webdriver.Chrome('./chromedriver')

    # Accede a route details add
    driver.get("https://ppointapi.clicoh.com/admin/driver/routedetail/add/")

    driver.implicitly_wait(10)

    # Auth
    driver.find_element(By.XPATH, "//input[@type='text'][contains(@id,'username')]").send_keys("admin")
    driver.find_element(By.XPATH, "//input[@type='password'][contains(@id,'password')]").send_keys("P4t4g0n14-99")
    driver.find_element(By.XPATH, "//input[contains(@type,'submit')]").click()

    driver.implicitly_wait(10)

    for i in range(len(data)):

        driver.implicitly_wait(10)

        # add route
        driver.find_element(By.XPATH, "//span[contains(@aria-labelledby,'select2-id_route-container')]").click()
        driver.find_element(By.XPATH, "//input[contains(@class,'select2-search__field')]").send_keys(data[i][0])
        while not search(data[i][0], driver.find_element(By.XPATH, "(//li[contains(@role,'treeitem')])[1]").text):
            time.sleep(.5)
        driver.find_element(By.XPATH, "(//li[contains(@role,'treeitem')])[1]").click()

        # add package
        driver.find_element(By.XPATH, "//span[contains(@aria-labelledby,'select2-id_package-container')]").click()
        driver.find_element(By.XPATH, "//input[contains(@class,'select2-search__field')]").send_keys(data[i][1])
        while not search(data[i][1],
                         driver.find_element(By.XPATH, "(//li[contains(@role,'treeitem')])[1]").text):
            time.sleep(.8)
        driver.find_element(By.XPATH, "(//li[contains(@role,'treeitem')])[1]").click()

        # Select payload type
        select_payload = driver.find_element(By.XPATH, "//select[contains(@id,'id_payload_type')]")
        select = Select(select_payload)
        select.select_by_index("1")

        # Post route_Detail
        driver.find_element(By.XPATH, "//input[@value='Save']").click()

        if i != len(data) - 1:
            driver.get("https://ppointapi.clicoh.com/admin/driver/routedetail/add/")

    # Route sync
    for i in range(len(route)):
        driver.get("https://ppointapi.clicoh.com/admin/driver/route/")
        driver.find_element(By.XPATH, "//input[contains(@type,'text')]").send_keys(route[i])
        driver.find_element(By.XPATH, "//input[contains(@type,'submit')]").click()
        driver.find_element(By.XPATH, "//input[contains(@name,'_selected_action')]").click()
        select_action = driver.find_element(By.XPATH, "//select[contains(@name,'action')]")
        select = Select(select_action)
        select.select_by_index("2")
        driver.find_element(By.XPATH, "//button[@type='submit'][contains(.,'Go')]").click()


def sync_route(route_id: list):
    driver = webdriver.Chrome('./chromedriver')

    # Accede a route details add
    driver.get("https://ppointapi.clicoh.com/admin/driver/route/")

    driver.implicitly_wait(10)

    # Auth
    driver.find_element(By.XPATH, "//input[@type='text'][contains(@id,'username')]").send_keys("admin")
    driver.find_element(By.XPATH, "//input[@type='password'][contains(@id,'password')]").send_keys("P4t4g0n14-99")
    driver.find_element(By.XPATH, "//input[contains(@type,'submit')]").click()

    driver.implicitly_wait(10)

    for i in range(len(route_id)):

        driver.find_element(By.XPATH, "//input[contains(@type,'text')]").send_keys(route_id[i])
        driver.find_element(By.XPATH, "//input[contains(@type,'submit')]").click()
        driver.find_element(By.XPATH, "//input[contains(@name,'_selected_action')]").click()
        select_action = driver.find_element(By.XPATH, "//select[contains(@name,'action')]")
        select = Select(select_action)
        select.select_by_index("2")
        driver.find_element(By.XPATH, "//button[@type='submit'][contains(.,'Go')]").click()
        if i != len(route_id) - 1:
            driver.get("https://ppointapi.clicoh.com/admin/driver/route/")

