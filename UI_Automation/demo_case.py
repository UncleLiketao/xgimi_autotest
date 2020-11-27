from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

desired_caps = { }
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '8.0'
desired_caps['deviceName'] = '192.168.4.10:5555'
desired_caps['appPackage'] = 'com.xgimi.manager'
desired_caps['appActivity'] = '.ui.activitys.MainActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

wait = WebDriverWait(driver, 10, 0.5)
wait.until(EC.presence_of_element_located((By.ID, "com.xgimi.manager:id/app_uninstall_bt")))
driver.find_element_by_id("com.xgimi.manager:id/app_uninstall_bt").click()
wait.until(EC.invisibility_of_element_located((By.ID, "com.xgimi.manager:id/app_uninstall_bt")))
cur_activity = driver.current_activity
print(cur_activity)

driver.quit()
