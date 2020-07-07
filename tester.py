from selenium import webdriver
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.headless = True
driver = webdriver.Firefox(options=opts)
driver.get("https://api.ipify.org/")
my_ip = driver.find_element_by_tag_name("pre").text
print(my_ip)
driver.get("http://www2.ppomppu.co.kr/zboard/view.php?id=phone&no=3522969")

driver.quit()
