from asyncio import sleep

from aiohttp import ClientSession
from loguru import logger

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

    async def spin_the_wheel(self) -> None:
        json_data = {
            'gameId': '2',
            'userAddress': self.wallet_address,
        }
        async with ClientSession(headers=headers) as session:
            response = await session.post(
                url='https://basehunt.xyz/api/spin-the-wheel/execute',
                json=json_data,
                proxy=self.proxy.proxy_url if self.proxy else None
            )
            if response.status == 200:
                response_text = await response.json()

                earned_type = response_text['spinData']['lastSpinResult']['type']
                points_earned = response_text['spinData']['lastSpinResult']['points']
                logger.success(
                    f'You earned {points_earned} {"PTS" if earned_type == "POINTS" else "USDC"} from the last spin | [{self.wallet_address}]')
            elif response.status == 400:
                logger.error(f'Wait for cooldown | [{self.wallet_address}]')
        await sleep(5)
        await self.get_state()

    async def get_state(self) -> None:
        params = {
            'userAddress': self.wallet_address,
            'gameId': '2',
        }
        async with ClientSession(headers=headers) as session:
            await session.get(
                url='https://basehunt.xyz/api/profile/state',
                params=params,
                proxy=self.proxy.proxy_url if self.proxy else None
            )
