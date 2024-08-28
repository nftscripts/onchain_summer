import random
import secrets
from asyncio import sleep
from datetime import datetime

import pyuseragents
import pytz
from aiohttp import ClientSession
from eth_account.messages import encode_defunct
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


async def create_juicy_adventure_tx(self, contract: Contract) -> TxParams:
    headers = {
        'accept': 'text/plain',
        'accept-language': 'ru,en;q=0.9,ru-RU;q=0.8,en-US;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://gram.voyage',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://gram.voyage/game/juicyadventure',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': pyuseragents.random(),
    }

    async def get_nonce(proxy: Proxy | None) -> str:
        async with ClientSession(headers=headers) as session:
            response = await session.get(
                'https://gram.voyage/api/ocs/nonce',
                proxy=proxy.proxy_url if proxy else None
            )
            response_json = await response.json()
            nonce = response_json['data']['nonce']
            return nonce

    async def get_auth_token(nonce: str, proxy: Proxy | None) -> str:
        signature, formatted_time = await get_signature(nonce)
        json_data = {
            'message': {
                'domain': 'gram.voyage',
                'address': self.wallet_address,
                'statement': 'Sign in Grampus.',
                'uri': 'https://gram.voyage',
                'version': '1',
                'chainId': 8453,
                'nonce': nonce,
                'issuedAt': formatted_time,
            },
            'signature': signature,
        }
        async with ClientSession(headers=headers) as session:
            response = await session.post(
                'https://gram.voyage/api/ocs/verify',
                json=json_data,
                proxy=proxy.proxy_url if proxy else None
            )
            response_json = await response.json()
            token = response_json['data']['token']
            return token

    async def get_signature(nonce: str) -> tuple[str, str]:
        now_utc = datetime.now(tz=pytz.utc)
        formatted_time = now_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        text = f'gram.voyage wants you to sign in with your Ethereum account:\n{self.wallet_address}\n\nSign in Grampus.\n\nURI: https://gram.voyage\nVersion: 1\nChain ID: 8453\nNonce: {nonce}\nIssued At: {formatted_time}'
        signed_message = self.web3.eth.account.sign_message(encode_defunct(text=text),
                                                            private_key=self.private_key)
        signature = signed_message.signature.hex()
        return signature, formatted_time

    async def get_tx_signature(auth_token: str, proxy: Proxy | None) -> tuple[str, str, str]:
        headers.update({'authorization': f'Bearer {auth_token}'})
        json_data = {
            'address': self.wallet_address,
            'nonce': secrets.token_hex(8),
            'order': random.sample([1, 2, 3, 4, 5], 3)
        }
        async with ClientSession(headers=headers) as session:
            response = await session.post(
                'https://gram.voyage/api/ocs/minting',
                json=json_data,
                proxy=proxy.proxy_url if proxy else None
            )
            response_json = await response.json()
            token_id = response_json['data']['tokenId']
            rarity = response_json['data']['rarity']
            signature = response_json['data']['signature']
            return token_id, rarity, signature

    nonce = await get_nonce(self.proxy)
    auth_token = await get_auth_token(nonce, self.proxy)
    token_id, rarity, signature = await get_tx_signature(auth_token, self.proxy)

    tx = await contract.functions.mintJuicyPack(
        token_id,
        rarity,
        signature
    ).build_transaction({
        'value': 0,
        'nonce': await self.web3.eth.get_transaction_count(self.wallet_address),
        'from': self.wallet_address,
        'gasPrice': await self.web3.eth.gas_price
    })
    return tx
