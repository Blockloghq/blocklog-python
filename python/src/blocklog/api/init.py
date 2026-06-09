from blocklog.client import BlocklogClient
from blocklog.config import BlocklogConfig
from blocklog._global import set_client

def init(api_key: str, **kwargs) -> BlocklogClient:
    """
    Initialize the Blocklog SDK.
    """
    config = BlocklogConfig(api_key=api_key, **kwargs)
    client = BlocklogClient(config)
    set_client(client)
    return client
