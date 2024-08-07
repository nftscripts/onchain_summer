from abc import ABC

from aiohttp import ClientSession
from loguru import logger

from src.utils.proxy_manager import Proxy
from src.utils.user.account import Account
from src.utils import headers
from src.utils.wrappers.decorators import retry


class ABCBadge(ABC, Account):
    ERROR_MESSAGES = {
        1: 'You must own Stand With Crypto Membership NFT to collect this badge',
        2: 'You must join Coinbase One and verify your wallet to claim this badge',
        3: 'Mint Buildathon NFT first',
        4: 'You have to own 20 NFTs to collect this badge',
        5: 'You have to trade at least 5 different tokens to collect this badge',
        6: 'You must hold at least 100 USDC to collect this badge',
        7: 'You must have at least 10 TXs to collect this badge',
        8: 'You must have at least 50 TXs to collect this badge',
        9: 'You must have at least 100 TXs to collect this badge',
        10: 'You must have at least 1000 TXs to collect this badge',
    }

    def __init__(
            self,
            private_key: str,
            badge_id: int,
            proxy: Proxy | None
    ):
        self.badge_id = badge_id
        super().__init__(private_key=private_key, proxy=proxy)

    @retry(retries=3, delay=30, backoff=1.5)
    async def claim_badge(self) -> None:
        json_data = {
            'gameId': 2,
            'userAddress': self.wallet_address,
            'badgeId': str(self.badge_id),
        }
        async with ClientSession(headers=headers) as session:
            response = await session.post(
                url='https://basehunt.xyz/api/badges/claim',
                json=json_data,
                proxy=self.proxy.proxy_url if self.proxy else None
            )
            if response.status == 200:
                response_text = await response.json()
                message = response_text['message']
                if message == 'challenge-completed':
                    logger.success(f'Successfully claimed badge')
                else:
                    logger.error(f'Something went wrong | {response_text}')
            elif response.status == 400:
                error_message = self.ERROR_MESSAGES.get(self.badge_id, 'Unknown error')
                logger.error(f'{error_message} | [{self.wallet_address}]')
