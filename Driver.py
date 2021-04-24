from selenium import webdriver
from fake_useragent import UserAgent
from proxy import Proxy
import os

def make_driver():

    proxy = Proxy()
    print('adding a proxy')
    while proxy.test_proxy(proxy.proxy) != 1:
        proxy.cycle()
        print(f"Trying new proxy at: {proxy.proxy['http']}")
    prox = proxy.proxy['http'].split('//')[1]
    options = webdriver.ChromeOptions() 
    userAgent = UserAgent().random
    options.add_argument("start-maximized")
    options.add_argument('--proxy-server=%s' % prox)
    options.add_argument(f'user-agent={userAgent}')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, executable_path= os.path.split(__file__)[0] + "\\chromedriver.exe")
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })
    return driver


