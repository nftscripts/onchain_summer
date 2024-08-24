from aiohttp import ClientSession

from loguru import logger

from src.utils.proxy_manager import Proxy
from src.utils.user.account import Account
from src.utils import headers


class OCSClient(Account):
    def __init__(
            self,
            private_key: str,
            proxy: Proxy | None
    ):
        super().__init__(private_key, proxy=proxy)

    async def register(self, referral_code: str | None = None) -> None:
        data = ('{"metrics":[{'
                '"metric_name":"perf_web_vitals_tbt_poor",'
                f'"page_path":"/ocs?referral_id={referral_code}",'
                '"value":1,'
                '"tags":{"authed":"false","platform":"web","is_low_end_device":true,"is_low_end_experience":true,"page_key":"ocs","save_data":false,"service_worker":"supported","is_perf_metric":true,"locale":"ru-RU","project_name":"wallet_dapp","version_name":null},"type":"count"}'
                ']}')
        async with ClientSession(headers=headers) as session:
            await session.post(
                url='https://as.coinbase.com/metrics',
                data=data,
                proxy=self.proxy.proxy_url if self.proxy else None
            )

            json_data = {
                'gameId': 2,
                'userAddress': self.wallet_address,
                'referralId': referral_code,
            }

            response = await session.post(
                url='https://basehunt.xyz/api/profile/opt-in',
                json=json_data,
                proxy=self.proxy.proxy_url if self.proxy else None
            )
            if response.status == 200:
                logger.success(f'Successfully registered wallet | [{self.wallet_address}]')
