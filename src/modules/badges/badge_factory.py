from src.utils.abc.abc_badge import ABCBadge
from src.utils.proxy_manager import Proxy


def create_badge_class(name: str, badge_id: int) -> object:
    def __init__(self, private_key: str, proxy: Proxy | None):
        super(badge_class, self).__init__(private_key=private_key, badge_id=badge_id, proxy=proxy)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} | [{self.wallet_address}]'

    badge_class = type(name, (ABCBadge,), {
        '__init__': __init__,
        '__str__': __str__,
    })
    return badge_class


StandWithCryptoBadge = create_badge_class('StandWithCryptoBadge', 1)
CoinbaseOneBadge = create_badge_class('CoinbaseOneBadge', 2)
BuildathonBadge = create_badge_class('BuildathonBadge', 3)
CollectorBadge = create_badge_class('CollectorBadge', 4)
TraderBadge = create_badge_class('TraderBadge', 5)
SaverBadge = create_badge_class('SaverBadge', 6)
TX10Badge = create_badge_class('TX10Badge', 7)
TX50Badge = create_badge_class('TX50Badge', 8)
TX100Badge = create_badge_class('TX100Badge', 9)
TX1000Badge = create_badge_class('TX1000Badge', 10)
