from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    # api_client = providers.Singleton(
    #     ApiClient,
    #     api_key=config.api_key,
    #     timeout=config.timeout,
    # )

    # service = providers.Factory(
    #     Service,
    #     api_client=api_client,
    # )
        

