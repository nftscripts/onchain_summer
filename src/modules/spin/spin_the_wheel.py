from asyncio import sleep

from aiohttp import ClientSession
from loguru import logger

from selenium_driverless.webdriver import Chrome
from selenium_driverless.types.by import By

from src.modules.spin.utils.driver import create_driver
from src.utils.proxy_manager import Proxy
from src.utils.user.account import Account
from src.utils import headers


class Wheel(Account):
    def __init__(
            self,
            private_key: str,
            proxy: Proxy | None
    ):
        super().__init__(private_key, proxy=proxy)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} | [{self.wallet_address}]'

    async def get_data(self) -> tuple[bool, str, str] | None:
        params = {
            'gameId': '2',
            'userAddress': self.wallet_address,
        }
        try:
            async with ClientSession(headers=headers) as session:
                response = await session.get(
                    'https://basehunt.xyz/api/spin-the-wheel',
                    params=params,
                    proxy=self.proxy.proxy_url if self.proxy else None
                )
                if response.status == 200:
                    response_json = await response.json()

                    spin_data = response_json['spinData']['lastSpinResult']
                    has_available_spin = response_json['spinData']['hasAvailableSpin']
                    if spin_data:
                        earned_type = spin_data['type']
                        points_earned = spin_data['points']
                    else:
                        earned_type = None
                        points_earned = None
                    return has_available_spin, earned_type, points_earned

                else:
                    return

        except TypeError as e:
            logger.error(f"Failed to get data: {e}")
            return

    async def check_level(self) -> int:
        params = {
            'userAddress': self.wallet_address,
            'gameId': '2',
        }
        async with ClientSession(headers=headers) as session:
            response = await session.get(
                url='https://basehunt.xyz/api/profile/state',
                params=params,
                proxy=self.proxy.proxy_url if self.proxy else None
            )
            if response.status == 200:
                response_json = await response.json()
                if response_json['isOptedIn'] is False:
                    return 0
                level = int(response_json['levelData']['level'])
                return level

    async def run_wallet(self) -> None:
        level = await self.check_level()
        if level is None:
            return
        if level < 1:
            logger.error(f'Your must have at least level 1 to spin the wheel. | [{self.wallet_address}]')
            return

        try:
            has_available_spin, _, _ = await self.get_data()
        except TypeError:
            return

        if not has_available_spin:
            logger.warning(f"You don't have available spin yet | [{self.wallet_address}]")
            return
        while True:
            driver = await create_driver(self.proxy)
            async with driver:
                try:
                    await driver.get('https://wallet.coinbase.com/', wait_load=True)
                    await self.connect_wallet(driver)
                    await sleep(20)
                    await self.spin_the_wheel(driver)
                    await sleep(20)
                    await driver.close()
                    _, earned_type, points_earned = await self.get_data()
                    logger.success(
                        f'You earned {points_earned} {"PTS" if earned_type == "POINTS" else "USDC"} '
                        f'from the last spin | [{self.wallet_address}]'
                    )
                    break

                except Exception as ex:
                    await driver.close()
                    if "didn't load within" in str(ex):
                        await sleep(10)
                        continue
                    logger.error(f"An error occurred: {ex}")
                    await sleep(10)
                    continue

    @staticmethod
    async def spin_the_wheel(driver: Chrome) -> None:
        windows = await driver.window_handles
        for window in windows:
            if window.title == 'Coinbase Wallet':
                await driver.switch_to.window(window)

        spin_to_earn_points_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[1]/button',
            timeout=60
        )
        await spin_to_earn_points_button.scroll_to()
        await spin_to_earn_points_button.click(move_to=True)
        await sleep(5)

        spin_the_wheel_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div/div[2]/div/div/button',
            timeout=60
        )
        await spin_the_wheel_button.click()
        await sleep(20)

    async def connect_wallet(self, driver: Chrome) -> None:
        await sleep(10)

        windows = await driver.window_handles
        for window in windows:
            if window.title == 'Coinbase Wallet':
                await driver.switch_to.window(window)

        await sleep(5)
        while True:
            try:
                next_button = await driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div/div/button',
                    timeout=60
                )
                await next_button.click(move_to=True)
                break
            except Exception as e:
                logger.error(f"Failed to find next button: {e}")
                await driver.refresh()
                await sleep(10)

        await self.perform_wallet_connection(driver)

    async def perform_wallet_connection(self, driver: Chrome) -> None:
        next_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div/div[2]/button',
            timeout=60
        )
        await next_button.click(move_to=True)

        get_started_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/div/div/div[2]/div/div[2]/div/div[2]/button[2]',
            timeout=60
        )
        await get_started_button.click(move_to=True)

        await sleep(10)

        coinbase_wallet_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div[1]/div[2]/div/div/div/ul/li[1]/button/div/div[2]',
            timeout=60
        )
        await coinbase_wallet_button.click(move_to=True)

        extension_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div[2]/div[2]/button/div/div[2]',
            timeout=60
        )
        await extension_button.click(move_to=True)

        await sleep(10)

        windows = await driver.window_handles
        await driver.switch_to.window(windows[0])

        await self.import_wallet_with_private_key(driver)

    async def import_wallet_with_private_key(self, driver: Chrome) -> None:
        already_have_wallet_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[1]/div[2]/ul/li[2]/button',
            timeout=60
        )
        await already_have_wallet_button.click(move_to=True)

        private_key_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div/button[1]/div/div/p[1]',
            timeout=60
        )
        await private_key_button.click(move_to=True)

        await sleep(2)

        agree_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[3]/div[1]/div/div/div[2]/div/div/div/div[2]/button',
            timeout=60
        )
        await agree_button.click(move_to=True)

        private_key_field = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div/div[1]/div/div/div/span/input',
            timeout=60
        )
        await private_key_field.send_keys(self.private_key, click_on=True)

        await sleep(5)

        import_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div[3]/button/span/span/span',
            timeout=60
        )
        await import_button.click(move_to=True)

        await self.setup_wallet_password(driver)

    @staticmethod
    async def setup_wallet_password(driver: Chrome) -> None:
        await sleep(10)
        password = 'ERTWRTEDFGa@8'

        password_field = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/div/span/input',
            timeout=60
        )
        await password_field.send_keys(password, click_on=True)

        password_repeat_field = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/div/span/input',
            timeout=60
        )
        await password_repeat_field.send_keys(password, click_on=True)

        check_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/label/div[1]/input',
            timeout=60
        )
        await check_button.click(move_to=True)

        send_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div[2]/div[2]/button',
            timeout=60
        )
        await send_button.click(move_to=True)

        await sleep(10)

        connect_button = await driver.find_element(
            By.XPATH,
            '/html/body/div[1]/div/div/div[2]/div/div[2]/div/div/div/div[3]/div/ul/li[2]/button',
            timeout=60
        )
        await connect_button.click(move_to=True)
