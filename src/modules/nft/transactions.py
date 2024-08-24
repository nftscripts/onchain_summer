from asyncio import sleep

import pyuseragents
from aiohttp import ClientSession
from eth_typing import ChecksumAddress
from web3.contract import Contract
from web3.types import TxParams
from loguru import logger

from src.utils import headers
from src.utils.proxy_manager import Proxy


async def create_mint_with_comment_tx(self, contract: Contract) -> TxParams:
    tx = None
    try:
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
    except Exception as ex:
        logger.error(ex)
    return tx


async def create_claim_tx(self, contract: Contract, quantity_limit: int, value: int = 0) -> TxParams:
    tx = None
    try:
        tx = await contract.functions.claim(
            self.wallet_address,
            1,
            self.web3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'),
            value,
            [['0x0000000000000000000000000000000000000000000000000000000000000000'],
             quantity_limit,
             value,
             self.web3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE')],
            '0x'
        ).build_transaction({
            'value': value,
            'nonce': await self.web3.eth.get_transaction_count(self.wallet_address),
            'from': self.wallet_address,
            'gasPrice': await self.web3.eth.gas_price
        })
    except Exception as ex:
        logger.error(ex)
    return tx


async def get_transaction_data(
        mint_address: str, wallet_address: ChecksumAddress, proxy: Proxy | None
) -> tuple[str, str] | None:
    json_data = {
        'bypassSimulation': True,
        'mintAddress': mint_address,
        'network': 'networks/base-mainnet',
        'quantity': '1',
        'takerAddress': wallet_address,
        'tokenId': '0',
    }
    headers.update({'user-agent': pyuseragents.random()})
    async with ClientSession(headers=headers) as session:
        response = await session.post(
            url='https://api.wallet.coinbase.com/rpc/v3/creators/mintToken',
            json=json_data,
            proxy=proxy.proxy_url if proxy else None
        )
        if response.status == 200:
            response_text = await response.json()
            data = response_text['callData']['data']
            value = response_text['callData']['value']
            return data, value
        elif response.status == 403:
            if proxy:
                if proxy.change_link:
                    await proxy.change_ip()
                    await sleep(5)


async def create_mint_tx_with_request(self, contract: Contract, mint_address: str) -> TxParams:
    transaction_data, value = None, None
    while True:
        try:
            transaction_data, value = await get_transaction_data(mint_address, self.wallet_address, self.proxy)
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
    try:
        gas = await self.web3.eth.estimate_gas(tx)
        tx.update({'gas': int(gas * 1.05)})
        return tx
    except ValueError as ex:
        if 'insufficient' in str(ex):
            logger.error(f'Nou enough money for mint | [{self.wallet_address}]')
