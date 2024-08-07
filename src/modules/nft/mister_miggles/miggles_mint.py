from asyncio import sleep

import pyuseragents
from web3.contract import Contract
from aiohttp import ClientSession
from web3.types import TxParams

from src.utils.abc.abc_mint import ABCOnchainSummer
from src.utils.proxy_manager import Proxy
from src.models.contracts import MisterMigglesData
from src.utils import headers


class MisterMigglesNFT(ABCOnchainSummer):
    def __init__(
            self,
            private_key: str,
            proxy: Proxy | None,
            name: str = 'Mister Miggles'
    ):
        contract_address = MisterMigglesData.address
        abi = MisterMigglesData.abi

        super().__init__(
            private_key=private_key,
            proxy=proxy,
            contract_address=contract_address,
            abi=abi,
            name=name,
            challenge_ids=['ocsChallenge_d0778cee-ad0b-46b9-93d9-887b917b2a1f']
        )

    def __str__(self) -> str:
        return f'{self.__class__.__name__} | [{self.wallet_address}]'

    async def get_transaction_data(self) -> tuple[str, str] | None:
        json_data = {
            'bypassSimulation': True,
            'mintAddress': '0xDc03a75F96f38615B3eB55F0F289d36E7A706660',
            'network': 'networks/base-mainnet',
            'quantity': '1',
            'takerAddress': self.wallet_address,
            'tokenId': '0',
        }
        headers.update({'user-agent': pyuseragents.random()})
        async with ClientSession(headers=headers) as session:
            response = await session.post(
                url='https://api.wallet.coinbase.com/rpc/v3/creators/mintToken',
                json=json_data,
                proxy=self.proxy.proxy_url if self.proxy else None
            )
            if response.status == 200:
                response_text = await response.json()
                data = response_text['callData']['data']
                value = response_text['callData']['value']
                return data, value
            elif response.status == 403:
                if self.proxy.change_link:
                    await self.proxy.change_ip()
                    await sleep(5)

    async def create_mint_tx(self, contract: Contract) -> TxParams:
        transaction_data, value = None, None
        while True:
            try:
                transaction_data, value = await self.get_transaction_data()
                break
            except TypeError:
                await sleep(5)
                continue

        if not (transaction_data or value):
            return
        tx = {
            'from': self.wallet_address,
            'value': int(value, 16),
            'to': self.web3.to_checksum_address(self.contract_address),
            'nonce': await self.web3.eth.get_transaction_count(self.wallet_address),
            'chainId': await self.web3.eth.chain_id,
            'gasPrice': await self.web3.eth.gas_price,
            'data': transaction_data
        }
        gas = await self.web3.eth.estimate_gas(tx)
        tx.update({'gas': int(gas * 1.05)})
        return tx
