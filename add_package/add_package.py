
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

import time

from selenium import webdriver


#P4t4g0n14-99

driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.



#Accede a routedetails_add
driver.get("https://release--api.clicoh.com/admin/driver/routedetail/add/")

driver.find_element(By.XPATH,"//input[@type='text'][contains(@id,'username')]").send_keys("admin")
sleep(2)
driver.find_element(By.XPATH,"//input[@type='password'][contains(@id,'password')]").send_keys("P4t4g0n14-99")
sleep(2)

driver.find_element(By.XPATH,"//input[contains(@type,'submit')]").click()
sleep(10)


#Click en ruta
driver.find_element(By.XPATH,"//span[contains(@aria-labelledby,'select2-id_route-container')]").click()
sleep(3)

#Busca ruta
driver.find_element(By.XPATH,"//input[contains(@class,'select2-search__field')]").send_keys("22")
sleep(3)

#Click en el primer elemento
driver.find_element(By.XPATH,"(//li[contains(@role,'treeitem')])[1]").click()
sleep(3)


#Click on package
driver.find_element(By.XPATH,"(//span[contains(@aria-labelledby,'select2-id_package-container')]").click()
sleep(15)

#Escribe codigo paquete
driver.find_element(By.XPATH,"(//input[contains(@class,'select2-search__field')]").send_keys("xyloh")
sleep(15)


#Click en el primer elemento
driver.find_element(By.XPATH,"(//li[contains(@role,'treeitem')])[1]").click()
sleep(10)


#Click en payload type
#driver.find_element(By.XPATH,"//select[@name='payload_type'][contains(@id,'type')]").click()

#Escribe stop number
driver.find_element(By.XPATH,"//input[@type='number'][contains(@id,'number')]").send_keys("9")
sleep(10)


#Guarda route detail
driver.find_element(By.XPATH,"//input[@value='Save']").click()
sleep(30)






