from dataclasses import dataclass


@dataclass
class ERC20:
    abi: str = open('./assets/abi/erc20.json', 'r').read()


@dataclass
class USABasketballData:
    address: str = '0x2aa80a13395425EF3897c9684a0249a5226eA779'
    abi: str = open('./assets/abi/basketball.json', 'r').read()


@dataclass
class MisterMigglesData:
    address: str = '0x1aeD60A97192157fDA7fb26267A439d523d09c5e'
    abi: str = open('./assets/abi/miggles.json', 'r').read()


@dataclass
class EthEtfData:
    address: str = '0xb5408b7126142C61f509046868B1273F96191b6d'
    abi: str = open('./assets/abi/eth_etf.json', 'r').read()


@dataclass
class ToshiData:
    address: str = '0xE65dFa5C8B531544b5Ae4960AE0345456D87A47D'
    abi: str = open('./assets/abi/eth_etf.json', 'r').read()


@dataclass
class EURCData:
    address: str = '0x615194d9695d0c02Fc30a897F8dA92E17403D61B'
    abi: str = open('./assets/abi/eth_etf.json', 'r').read()


@dataclass
class TreasureChestData:
    address: str = '0x2E2c0753fc81BE22381c674ADD7A05F24cfD9761'
    abi: str = open('./assets/abi/treasure_chest.json', 'r').read()


@dataclass
class LiquidData:
    address: str = '0x1aeD60A97192157fDA7fb26267A439d523d09c5e'
    abi: str = open('./assets/abi/miggles.json', 'r').read()


@dataclass
class ETHCantBeStoppedData:
    address: str = '0xb0FF351AD7b538452306d74fB7767EC019Fa10CF'
    abi: str = open('./assets/abi/eth_etf.json', 'r').read()


@dataclass
class BuildathonData:
    address: str = '0x1aeD60A97192157fDA7fb26267A439d523d09c5e'
    abi: str = open('./assets/abi/miggles.json', 'r').read()


@dataclass
class HappyNouniversaryData:
    address: str = '0xE0fE6DD851187c62a79D00a211953Fe3B5Cec7FE'
    abi: str = open('./assets/abi/eth_etf.json', 'r').read()
