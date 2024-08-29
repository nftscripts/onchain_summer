from asyncio import wait_for, TimeoutError
from loguru import logger

from src.modules.spin.spin_the_wheel import Wheel
from src.utils.proxy_manager import Proxy
from src.modules.ocs.ocs_client import OCSClient
from config import referral_code

from src.modules.nft.nft_factory import (
    IntroducingCoinbaseWalletWebApp,
    MisterMigglesNFT,
    EthEtfNFT,
    JuicyAdventure,
    TheWorldAfterEthEtfApproval,
    ETHCantBeStoppedNFT,
    EthereumETF,
    ToshiNFT,
    EurcNFT,
    LiquidNFT,
    BuildathonNFT,
    ETFEREUM,
    HappyNouniversaryNFT,
    PoolTogetherNFT,
    StixLaunchNFT,
    Forbes
)
from src.modules.badges.badge_factory import (
    StandWithCryptoBadge,
    CoinbaseOneBadge,
    BuildathonBadge,
    CollectorBadge,
    TraderBadge,
    SaverBadge,
    TX10Badge,
    TX50Badge,
    TX100Badge,
    TX1000Badge,
)


def create_process_function(NFTClass, method_name='mint'):
    async def process(private_key: str, proxy: Proxy | None) -> None:
        nft_instance = NFTClass(
            private_key=private_key,
            proxy=proxy
        )
        logger.debug(nft_instance)
        try:
            await wait_for(
                fut=getattr(nft_instance, method_name)(),
                timeout=600
            )
        except TimeoutError:
            logger.error(f'{nft_instance} timed out')

    return process


process_coinbase_wallet_web_app_mint = create_process_function(IntroducingCoinbaseWalletWebApp)
process_ethereum_etf_mint = create_process_function(EthereumETF)
process_etfereum_mint = create_process_function(ETFEREUM)
process_world_after_etf_approval_mint = create_process_function(TheWorldAfterEthEtfApproval)
process_mister_miggles_mint = create_process_function(MisterMigglesNFT)
process_eth_etf_mint = create_process_function(EthEtfNFT)
process_toshi_mint = create_process_function(ToshiNFT)
process_eurc_mint = create_process_function(EurcNFT)
process_liquid_mint = create_process_function(LiquidNFT)
process_eth_cant_be_stopped_mint = create_process_function(ETHCantBeStoppedNFT)
process_buildathon_mint = create_process_function(BuildathonNFT)
process_happy_nouniversary_mint = create_process_function(HappyNouniversaryNFT)
process_pool_together_mint = create_process_function(PoolTogetherNFT)
process_stix_launch_mint = create_process_function(StixLaunchNFT)
process_juicy_adventure_mint = create_process_function(JuicyAdventure)
process_forbes_mint = create_process_function(Forbes)

process_stand_with_crypto_badge = create_process_function(StandWithCryptoBadge, 'claim_badge')
process_coinbase_one_badge = create_process_function(CoinbaseOneBadge, 'claim_badge')
process_buildathon_badge = create_process_function(BuildathonBadge, 'claim_badge')
process_collector_badge = create_process_function(CollectorBadge, 'claim_badge')
process_trader_badge = create_process_function(TraderBadge, 'claim_badge')
process_saver_badge = create_process_function(SaverBadge, 'claim_badge')
process_10tx_badge = create_process_function(TX10Badge, 'claim_badge')
process_50tx_badge = create_process_function(TX50Badge, 'claim_badge')
process_100tx_badge = create_process_function(TX100Badge, 'claim_badge')
process_1000tx_badge = create_process_function(TX1000Badge, 'claim_badge')

process_wheel = create_process_function(Wheel, 'spin_the_wheel')


async def process_register(private_key: str, proxy: Proxy | None) -> None:
    ocs_client = OCSClient(
        private_key=private_key,
        proxy=proxy
    )
    await ocs_client.register(referral_code=referral_code)
