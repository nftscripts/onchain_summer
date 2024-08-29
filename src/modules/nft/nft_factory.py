from typing import Callable

from web3.contract import Contract
from web3.types import TxParams

from src.utils.abc.abc_mint import ABCOnchainSummer
from src.utils.proxy_manager import Proxy
from src.models.contracts import *

from src.modules.nft.transactions import (
    create_mint_with_comment_tx,
    create_claim_tx,
    create_mint_tx_with_request,
    create_juicy_adventure_tx
)


def create_nft_class(
        class_name: str,
        contract_data,
        name: str,
        challenge_ids: list[str],
        mint_tx_function: Callable
) -> type:
    class NFTClass(ABCOnchainSummer):
        def __init__(self, private_key: str, proxy: Proxy | None):
            contract_address = contract_data.address
            abi = contract_data.abi

            super().__init__(
                private_key=private_key,
                proxy=proxy,
                contract_address=contract_address,
                abi=abi,
                name=name,
                challenge_ids=challenge_ids
            )

        def __str__(self) -> str:
            return f'{self.__class__.__name__} | [{self.wallet_address}]'

        async def create_mint_tx(self, contract: Contract) -> TxParams:
            return await mint_tx_function(self, contract)

    NFTClass.__name__ = class_name
    return NFTClass


BuildathonNFT = create_nft_class(
    class_name='BuildathonNFT',
    contract_data=BuildathonData,
    name='BuildathonNFT',
    challenge_ids=None,
    mint_tx_function=lambda self, contract: create_mint_tx_with_request(
        self, contract, '0x0c45CA58cfA181b038E06dd65EAbBD1a68d3CcF3'
    )
)

ETHCantBeStoppedNFT = create_nft_class(
    class_name='ETHCantBeStoppedNFT',
    contract_data=ETHCantBeStoppedData,
    name="ETH Can't Be Stopped",
    challenge_ids=['ocsChallenge_c1de2373-35ad-4f3c-ab18-4dfadf15754d'],
    mint_tx_function=create_mint_with_comment_tx
)

EthEtfNFT = create_nft_class(
    class_name='EthEtfNFT',
    contract_data=EthEtfData,
    name="ETH ETF",
    challenge_ids=['5e383RWcRtGAwGUorkGiYC'],
    mint_tx_function=create_mint_with_comment_tx
)

EurcNFT = create_nft_class(
    class_name='EurcNFT',
    contract_data=EURCData,
    name='EURC x Base Launch',
    challenge_ids=['1iZiHPbqaIGW5F08bCit6J'],
    mint_tx_function=create_mint_with_comment_tx
)

ToshiNFT = create_nft_class(
    class_name='ToshiNFT',
    contract_data=ToshiData,
    name='Happy Birthday Toshi',
    challenge_ids=['1pjoNf5onjgsi7r9fWp3ob'],
    mint_tx_function=create_mint_with_comment_tx
)

HappyNouniversaryNFT = create_nft_class(
    class_name='HappyNouniversaryNFT',
    contract_data=HappyNouniversaryData,
    name='Happy Nouniversary',
    challenge_ids=['44wp1P8LSnwkPSz7Ft3q78'],
    mint_tx_function=create_mint_with_comment_tx
)

LiquidNFT = create_nft_class(
    class_name='LiquidNFT',
    contract_data=LiquidData,
    name='Liquid',
    challenge_ids=['6VRBNN6qr2algysZeorek8'],
    mint_tx_function=lambda self, contract: create_claim_tx(self, contract, 2)
)

MisterMigglesNFT = create_nft_class(
    class_name='MisterMigglesNFT',
    contract_data=MisterMigglesData,
    name='Mister Miggles',
    challenge_ids=['ocsChallenge_d0778cee-ad0b-46b9-93d9-887b917b2a1f'],
    mint_tx_function=lambda self, contract: create_mint_tx_with_request(
        self,
        contract,
        mint_address='0xDc03a75F96f38615B3eB55F0F289d36E7A706660'
    )
)

PoolTogetherNFT = create_nft_class(
    class_name='PoolTogetherNFT',
    contract_data=PoolTogetherData,
    name='Pool Together',
    challenge_ids=['ocsChallenge_2f2ea707-d664-4d4b-918b-6299bdf45cd8'],
    mint_tx_function=lambda self, contract: create_claim_tx(
        self,
        contract,
        115792089237316195423570985008687907853269984665640564039457584007913129639935
    )
)

StixLaunchNFT = create_nft_class(
    class_name='StixLaunchNFT',
    contract_data=StixLaunchData,
    name='STIX Launch Tournament Pass',
    challenge_ids=['ocsChallenge_bd5208b5-ff1e-4f5b-8522-c4d4ebb795b7'],
    mint_tx_function=lambda self, contract: create_claim_tx(
        self, contract, 1
    )
)

TheWorldAfterEthEtfApproval = create_nft_class(
    class_name='TheWorldAfterEthEtfApproval',
    contract_data=TheWorldAfterEthEtfApprovalData,
    name='the world after ETH ETF approval',
    challenge_ids=['ocsChallenge_65c17605-e085-4528-b4f1-76ce5f48da56'],
    mint_tx_function=create_mint_with_comment_tx
)

ETFEREUM = create_nft_class(
    class_name='ETFEREUM',
    contract_data=ETFEREUMData,
    name='ETFEREUM',
    challenge_ids=['ocsChallenge_eba9e6f0-b7b6-4d18-8b99-a64aea045117'],
    mint_tx_function=create_mint_with_comment_tx
)

EthereumETF = create_nft_class(
    class_name='EthereumETF',
    contract_data=EthereumETFData,
    name='Ethereum ETF',
    challenge_ids=['ocsChallenge_ee0cf23e-74a1-4bb3-badf-037a6bbf35e8'],
    mint_tx_function=create_mint_with_comment_tx
)

IntroducingCoinbaseWalletWebApp = create_nft_class(
    class_name='IntroducingCoinbaseWalletWebApp',
    contract_data=IntroducingCoinbaseWalletWebAppData,
    name='Introducing: Coinbase Wallet web app',
    challenge_ids=['78zcHkWSABcPWMoacVI9Vs'],
    mint_tx_function=lambda self, contract: create_claim_tx(
        self,
        contract,
        115792089237316195423570985008687907853269984665640564039457584007913129639935,
        value=int(0.0001 * 10 ** 18)
    )
)

JuicyAdventure = create_nft_class(
    class_name='JuicyAdventure',
    contract_data=JuicyAdventureData,
    name='Juicy Adventure',
    challenge_ids=['ocsChallenge_3b1c2886-3168-45c7-b2cd-b590cde66c61'],
    mint_tx_function=create_juicy_adventure_tx
)

Forbes = create_nft_class(
    class_name='Forbes',
    contract_data=ForbesData,
    name='Forbes Web3 INSPIRE',
    challenge_ids=['ocsChallenge_b3f47fc6-3649-4bad-9e10-7244fbe1d484'],
    mint_tx_function=lambda self, contract: create_claim_tx(
        self,
        contract,
        115792089237316195423570985008687907853269984665640564039457584007913129639935
    )
)
