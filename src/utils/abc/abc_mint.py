from abc import ABC, abstractmethod
from asyncio import sleep

from aiohttp import ClientSession
from web3.contract import Contract
from web3.types import TxParams
from loguru import logger

from src.utils.proxy_manager import Proxy
from src.utils.user.account import Account
from src.utils.wrappers.decorators import retry
from .. import headers


class ABCOnchainSummer(ABC, Account):
    def __init__(
            self,
            private_key: str,
            proxy: Proxy | None,
            contract_address: str,
            abi: str,
            name: str,
            challenge_ids: list[str]

    ):
        super().__init__(private_key=private_key, proxy=proxy)
        self.contract_address = contract_address
        self.abi = abi
        self.name = name
        self.challenge_ids = challenge_ids

    @abstractmethod
    async def create_mint_tx(self, contract: Contract) -> TxParams:
        """Creates transaction for mint"""

    @retry(retries=3, delay=30, backoff=1.5)
    async def mint(self) -> None:
        balance = await self.get_wallet_balance('ETH', '...')
        if balance == 0:
            logger.error(f'Your ETH balance is 0 | [{self.wallet_address}]')
            return

        contract = self.load_contract(
            address=self.contract_address,
            web3=self.web3,
            abi=self.abi
        )

        tx = await self.create_mint_tx(contract)

        if tx is None:
            return

        try:
            tx_hash = await self.sign_transaction(tx)
            confirmed = await self.wait_until_tx_finished(tx_hash)
        except Exception as ex:
            logger.error(f'Something went wrong {ex}')
            return False

        if confirmed:
            logger.success(
                f'Successfully minted {self.name} NFT | TX: https://basescan.org/tx/{tx_hash}'
            )
            await sleep(5)
            if self.challenge_ids:
                await self.claim_points(self.challenge_ids)

    async def claim_points(self, challenge_ids: list[str]) -> None:
        for challenge_id in challenge_ids:
            json_data = {
                'gameId': 2,
                'userAddress': self.wallet_address,
                'challengeId': challenge_id,
            }
            while True:
                async with ClientSession(headers=headers) as session:
                    response = await session.post(
                        url='https://basehunt.xyz/api/challenges/complete',
                        json=json_data,
                        proxy=self.proxy.proxy_url if self.proxy else None
                    )
                    response_text = await response.json()
                    if response.status == 200:
                        message = response_text['message']
                        if message == 'challenge-completed' or message == 'challenge-claimed':
                            logger.success(f'Successfully claimed points for {self.name} NFT | [{self.wallet_address}]')
                            break
                        else:
                            await sleep(5)
                            continue
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
