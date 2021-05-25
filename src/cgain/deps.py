from dependency_injector import containers, providers

from cgain.infrastructure.adapter.exchange import BinanceExchange


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    exchange = providers.Singleton(
        BinanceExchange, api_key=config.api_key, secret_key=config.secret_key
    )
