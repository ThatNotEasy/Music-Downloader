from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from modules.logging import setup_logging
from colorama import Fore, Style

logging = setup_logging()

def setup_driver(browser):
    try:
        extension_path = r"extension\2.0.4_0.crx"
        if browser == 'chrome':
            options = ChromeOptions()
            options.add_extension(extension_path)
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-webgl")
            options.add_argument('--enable-unsafe-swiftshader')
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        
        elif browser == 'firefox':
            options = FirefoxOptions()
            options.headless = True
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        
        elif browser == 'edge':
            options = EdgeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument("--disable-logging")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

        elif browser == 'brave':
            options = ChromeOptions()
            options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            options.add_extension(extension_path)
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-webgl")
            options.add_argument('--enable-unsafe-swiftshader')
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        
        else:
            return None

        return driver
    except Exception as e:
        logging.error(f"{Fore.RED}Failed to initialize {browser} browser{Style.RESET_ALL}")
        return None