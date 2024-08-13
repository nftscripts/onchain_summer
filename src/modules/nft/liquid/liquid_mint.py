from web3.contract import Contract
from web3.types import TxParams

from src.utils.abc.abc_mint import ABCOnchainSummer
from src.utils.proxy_manager import Proxy
from src.models.contracts import LiquidData


class LiquidNFT(ABCOnchainSummer):
    def __init__(
            self,
            private_key: str,
            proxy: Proxy | None,
            name: str = 'Liquid'
    ):
        contract_address = LiquidData.address
        abi = LiquidData.abi

        super().__init__(
            private_key=private_key,
            proxy=proxy,
            contract_address=contract_address,
            abi=abi,
            name=name,
            challenge_ids=['6VRBNN6qr2algysZeorek8']
        )

    def __str__(self) -> str:
        return f'{self.__class__.__name__} | [{self.wallet_address}]'

    async def create_mint_tx(self, contract: Contract) -> TxParams:
        tx = await contract.functions.claim(
            self.wallet_address,
            1,
            self.web3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'),
            0,
            [['0x0000000000000000000000000000000000000000000000000000000000000000'],
             2,
             0,
             self.web3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE')],
            '0x'
        ).build_transaction({
            'value': 0,
            'nonce': await self.web3.eth.get_transaction_count(self.wallet_address),
            'from': self.wallet_address,
            'gasPrice': await self.web3.eth.gas_price
        })
        return tx
