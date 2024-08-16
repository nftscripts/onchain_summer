from src.utils.runner import *

module_handlers = {
    'basketball_nft': process_basketball_mint,
    'mister_miggles_nft': process_mister_miggles_mint,
    'celebrating_the_ethereum_etf': process_eth_etf_mint,
    'happy_birthday_toshi': process_toshi_mint,
    'happy_nouniversary': process_happy_nouniversary_mint,
    'eurc_x_base_launch': process_eurc_mint,
    'treasure_chest_mint': process_treasure_mint,
    'team_liquid_premiere_series': process_liquid_mint,
    'stix_launch_tournament_pass': process_stix_launch_mint,
    'eth_cant_be_stopped': process_eth_cant_be_stopped_mint,
    'pool_together': process_pool_together_mint,
    'buildathon': process_buildathon_mint,
    'stand_with_crypto_badge': process_stand_with_crypto_badge,
    'coinbase_one_badge': process_coinbase_one_badge,
    'buildathon_badge': process_buildathon_badge,
    'collector_badge': process_collector_badge,
    'trader_badge': process_trader_badge,
    'saver_badge': process_saver_badge,
    'based_10_txs': process_10tx_badge,
    'based_50_txs': process_50tx_badge,
    'based_100_txs': process_100tx_badge,
    'based_1000_txs': process_1000tx_badge,
    'spin_the_wheel': process_wheel
}
