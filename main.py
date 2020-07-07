import os
from multiprocessing import Process, Queue

from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent

import random, time
import requests

url = ''
minutes = 0
used_ip = {}

def runBrowser(n, q):
    global url
    global minutes
    while True:
        try:
            with Controller.from_port(port=9053 + n * 2) as c:
                c.authenticate("steamviewbot")
                c.signal(Signal.NEWNYM)
            socks = 'socks5://127.0.0.1:' + str(9052 + n * 2)
            proxies = {
                'http': socks,
                'https': socks
            }

            my_ip = requests.get('https://api.ipify.org', proxies=proxies).text
            if my_ip in used_ip:
                continue
            else:
                used_ip[my_ip] = 0
    
                opts = Options()
                opts.log.level = "trace"
                opts.headless = True
                profile = webdriver.FirefoxProfile()
                profile.set_preference("network.proxy.type", 1)
                profile.set_preference("network.proxy.socks", "127.0.0.1")
                profile.set_preference("network.proxy.socks_port", 9052 + n * 2)
                profile.set_preference('general.useragent.override', UserAgent().random)
                profile.update_preferences()
                driver = webdriver.Firefox(profile, options=opts)
                driver.get(url)
                # data = driver.find_element_by_xpath('/html/body/div/div[2]/div[4]/div/table[2]/tbody/tr[3]/td/table/tbody/tr/td[5]/br[6]')
                # data = [driver.page_source]

                q.put(my_ip)
                wait = random.randrange(minutes * 60, int(minutes*1.2) * 60)
                # wait = random.randrange(60, 120)
                time.sleep(wait)
                driver.stop_client()
                driver.close()
                driver.quit()
        except:
            pass


if __name__ == '__main__':
    url = input("URL : ")
    minutes = input("Time to stay in a page (min) : ")
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'shared_preferences')
    shared = open(filename, 'r')
    line = shared.readline()
    print(line)
    process_count = int(line.strip())
    shared.close()

    view_count = 0
    out_queue = Queue()
    browserProcess = []
    for i in range(process_count):
        browserProcess.append(Process(target=runBrowser, args=(i, out_queue,)))
        browserProcess[i].start()

    try:
        while True:
            my_ip = out_queue.get()
            view_count += 1
            print('VIEW COUNT : %d \t %s' % (view_count, my_ip))
    except KeyboardInterrupt:
        out_queue.close()
        out_queue.join_thread()
        for i in range(0, process_count):
            browserProcess[i].join()
