    
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

driver = webdriver.Chrome('./chromedriver') 

#Accede a routedetails_add
driver.get("https://release--api.clicoh.com/admin/driver/routedetail/add/")

driver.implicitly_wait(10)

#Auth
driver.find_element(By.XPATH,"//input[@type='text'][contains(@id,'username')]").send_keys("admin")
driver.find_element(By.XPATH,"//input[@type='password'][contains(@id,'password')]").send_keys("P4t4g0n14-99")
time.sleep(1)
driver.find_element(By.XPATH,"//input[contains(@type,'submit')]").click()


route_id = 12
stop_number = 1
package_code = "xyloh"



driver.implicitly_wait(10)

#Click en ruta
driver.find_element(By.XPATH,"//span[contains(@aria-labelledby,'select2-id_route-container')]").click()


#Busca ruta
#Busca ruta
driver.find_element(By.XPATH,"//input[contains(@class,'select2-search__field')]").send_keys(route_id)
driver.implicitly_wait()


#Click en el primer elemento
driver.find_element(By.XPATH,"(//li[contains(@role,'treeitem')])[1]").click()


#Click on package
driver.find_element(By.XPATH,"//span[contains(@aria-labelledby,'select2-id_package-container')]").click()
driver.implicitly_wait(5)


#Escribe codigo paquete
driver.find_element(By.XPATH,"//input[contains(@class,'select2-search__field')]").send_keys(package_code)
driver.implicitly_wait(10)

        #Click en el primer elemento
driver.find_element(By.XPATH,"(//li[contains(@role,'treeitem')])[1]").click()
driver.implicitly_wait(10)

        #Click en payload type
select_payload = driver.find_element(By.XPATH,"//select[contains(@id,'id_payload_type')]")
select = Select(select_payload)
select.select_by_index("1")
driver.implicitly_wait(10)

        #borra stop number
driver.find_element(By.XPATH,"//input[@type='number'][contains(@id,'number')]").clear()
driver.implicitly_wait(10)

        #Escribe stop number
driver.find_element(By.XPATH,"//input[@type='number'][contains(@id,'number')]").send_keys(stop_number)
driver.implicitly_wait(10)

        #Guarda route detail
driver.find_element(By.XPATH,"//input[@value='Save']").click()
driver.implicitly_wait(10)

        #Accede a routedetails_add
driver.get("https://release--api.clicoh.com/admin/driver/routedetail/add/")
