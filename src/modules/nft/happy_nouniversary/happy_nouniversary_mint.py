from web3.contract import Contract
from web3.types import TxParams

from src.utils.abc.abc_mint import ABCOnchainSummer
from src.utils.proxy_manager import Proxy
from src.models.contracts import HappyNouniversaryData


class HappyNouniversaryNFT(ABCOnchainSummer):
    def __init__(
            self,
            private_key: str,
            proxy: Proxy | None,
            name: str = 'Happy Nouniversary'
    ):
        contract_address = HappyNouniversaryData.address
        abi = HappyNouniversaryData.abi

        super().__init__(
            private_key=private_key,
            proxy=proxy,
            contract_address=contract_address,
            abi=abi,
            name=name,
            challenge_ids=['44wp1P8LSnwkPSz7Ft3q78']
        )

    def __str__(self) -> str:
        return f'{self.__class__.__name__} | [{self.wallet_address}]'

    async def create_mint_tx(self, contract: Contract) -> TxParams:
        tx = await contract.functions.mintWithComment(
            self.wallet_address,
            1,
            ''
        ).build_transaction({
            'value': int(0.0001 * 10 ** 18),
            'nonce': await self.web3.eth.get_transaction_count(self.wallet_address),
            'from': self.wallet_address,
            'gasPrice': await self.web3.eth.gas_price
        })
        return tx
