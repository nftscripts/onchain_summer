import pyuseragents

headers = {
    'accept': '*/*',
    'accept-language': 'ru,en;q=0.9,ru-RU;q=0.8,en-US;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://wallet.coinbase.com',
    'priority': 'u=1, i',
    'referer': 'https://wallet.coinbase.com/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': pyuseragents.random(),
}
