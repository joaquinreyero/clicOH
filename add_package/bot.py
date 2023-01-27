from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select


def basic_config_auth():

    driver = webdriver.Chrome('./chromedriver') 

    #Accede a routedetails_add
    driver.get("https://release--api.clicoh.com/admin/driver/routedetail/add/")

    driver.implicitly_wait(10)

    #Auth
    driver.find_element(By.XPATH,"//input[@type='text'][contains(@id,'username')]").send_keys("admin")
    driver.find_element(By.XPATH,"//input[@type='password'][contains(@id,'password')]").send_keys("P4t4g0n14-99")
    time.sleep(1)
    driver.find_element(By.XPATH,"//input[contains(@type,'submit')]").click()

    return driver

#Crear routes details
def add_route_details(driver,n,route_id,package_code,stop_number):

    for i in range(n):

        driver.implicitly_wait(10)

        #Click en ruta
        driver.find_element(By.XPATH,"//span[contains(@aria-labelledby,'select2-id_route-container')]").click()

        #Busca ruta
        driver.find_element(By.XPATH,"//input[contains(@class,'select2-search__field')]").send_keys(route_id)
        time.sleep(5)

        #Click en el primer elemento
        driver.find_element(By.XPATH,"(//li[contains(@role,'treeitem')])[1]").click()

        #Click on package
        driver.find_element(By.XPATH,"//span[contains(@aria-labelledby,'select2-id_package-container')]").click()


        #Escribe codigo paquete
        driver.find_element(By.XPATH,"//input[contains(@class,'select2-search__field')]").send_keys(package_code)
        time.sleep(15)

        #Click en el primer elemento
        driver.find_element(By.XPATH,"(//li[contains(@role,'treeitem')])[1]").click()

        #Click en payload type
        select_payload = driver.find_element(By.XPATH,"//select[contains(@id,'id_payload_type')]")
        select = Select(select_payload)
        select.select_by_index("1")
        time.sleep(1)

        #borra stop number
        driver.find_element(By.XPATH,"//input[@type='number'][contains(@id,'number')]").clear()
        time.sleep(1)


        #Escribe stop number
        driver.find_element(By.XPATH,"//input[@type='number'][contains(@id,'number')]").send_keys(stop_number)
        time.sleep(2)

        #Guarda route detail
        driver.find_element(By.XPATH,"//input[@value='Save']").click()
        time.sleep(6)

        #Accede a routedetails_add
        driver.get("https://release--api.clicoh.com/admin/driver/routedetail/add/")

    driver.exit()







