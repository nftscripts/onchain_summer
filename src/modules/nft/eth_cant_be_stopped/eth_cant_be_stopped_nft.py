from web3.contract import Contract
from web3.types import TxParams

from src.utils.abc.abc_mint import ABCOnchainSummer
from src.utils.proxy_manager import Proxy
from src.models.contracts import ETHCantBeStoppedData


class ETHCantBeStoppedNFT(ABCOnchainSummer):
    def __init__(
            self,
            private_key: str,
            proxy: Proxy | None,
            name: str = "ETH can't be stopped"
    ):
        contract_address = ETHCantBeStoppedData.address
        abi = ETHCantBeStoppedData.abi

        super().__init__(
            private_key=private_key,
            proxy=proxy,
            contract_address=contract_address,
            abi=abi,
            name=name,
            challenge_ids=['ocsChallenge_c1de2373-35ad-4f3c-ab18-4dfadf15754d']
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
            'gas': int(await self.web3.eth.gas_price)
        })
        return tx
