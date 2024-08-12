from asyncio import wait_for, TimeoutError
from loguru import logger

from src.modules.nft.eth_etf.eth_etf_mint import EthEtfNFT
from src.modules.nft.basketball.basketball_mint import BasketballNFT
from src.modules.nft.happy_birthday_toshi.toshi_mint import ToshiNFT
from src.modules.nft.eth_cant_be_stopped.eth_cant_be_stopped_nft import ETHCantBeStoppedNFT
from src.modules.nft.happy_nouniversary.happy_nouniversary_mint import HappyNouniversaryNFT
from src.modules.nft.treasure_chest.treasure_chest_mint import TreasureChestNFT
from src.modules.nft.pool_together.pool_together_mint import PoolTogetherNFT
from src.modules.nft.mister_miggles.miggles_mint import MisterMigglesNFT
from src.modules.nft.builathon.buildathon_nft import BuildathonNFT
from src.modules.nft.liquid.liquid_mint import LiquidNFT
from src.modules.nft.eurc.eurc_mint import EurcNFT
from src.modules.spin.spin_the_wheel import Wheel
from src.utils.proxy_manager import Proxy

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


process_basketball_mint = create_process_function(BasketballNFT)
process_mister_miggles_mint = create_process_function(MisterMigglesNFT)
process_eth_etf_mint = create_process_function(EthEtfNFT)
process_toshi_mint = create_process_function(ToshiNFT)
process_eurc_mint = create_process_function(EurcNFT)
process_treasure_mint = create_process_function(TreasureChestNFT)
process_liquid_mint = create_process_function(LiquidNFT)
process_eth_cant_be_stopped_mint = create_process_function(ETHCantBeStoppedNFT)
process_buildathon_mint = create_process_function(BuildathonNFT)
process_happy_nouniversary_mint = create_process_function(HappyNouniversaryNFT)
process_pool_together_mint = create_process_function(PoolTogetherNFT)


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
