
from selenium import webdriver


driver = webdriver.Firefox()
driver.get("https://api.ipify.org/")
my_ip = driver.find_element_by_tag_name("pre").text
print(my_ip)
driver.get("http://www2.ppomppu.co.kr/zboard/view.php?id=phone&no=3522969")

driver.quit()
