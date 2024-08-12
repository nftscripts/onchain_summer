from selenium_driverless.webdriver import Chrome
from selenium_driverless import webdriver

from src.utils.proxy_manager import Proxy
from config import ROTATE_IP


async def create_driver(proxy: Proxy | None) -> Chrome:
    options = webdriver.ChromeOptions()
    options.headless = True
    if proxy:
        if ROTATE_IP and proxy.change_link:
            await proxy.change_ip()
        options.single_proxy = proxy.proxy_url
    options.add_extension('src/modules/spin/utils/crx/coinbase_wallet.crx')
    driver = webdriver.Chrome(options=options)
    return driver
