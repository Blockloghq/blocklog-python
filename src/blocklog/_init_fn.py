"""
blocklog._init_fn
~~~~~~~~~~~~~~~~~
Implements the top-level ``blocklog.init()`` call.

Usage::

    import blocklog
    blocklog.init(api_key="blk_...")

    # or via environment variable BLOCKLOG_API_KEY
    blocklog.init()
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from blocklog.client import BlocklogClient


def init(
    api_key: str | None = None,
    *,
    base_url: str | None = None,
    signing_key: str | None = None,
    timeout: float | None = None,
    max_retries: int | None = None,
    debug: bool = False,
) -> "BlocklogClient":
    """Initialise the Blocklog SDK.

    Call once at application startup — typically right after your other
    infrastructure initialisation (logging, config loading, etc.).

    Parameters
    ----------
    api_key:
        Your Blocklog API key.  Falls back to the ``BLOCKLOG_API_KEY``
        environment variable when omitted.
    base_url:
        Override the default API base URL.  Useful for self-hosted
        deployments.  Falls back to ``BLOCKLOG_BASE_URL``.
    signing_key:
        Ed25519 private key used to sign log payloads for tamper-evidence.
        Falls back to ``BLOCKLOG_SDK_SIGNING_KEY``.
    timeout:
        Per-request timeout in seconds (default: 10).
    max_retries:
        Number of automatic retries on transient failures (default: 3).
    debug:
        When ``True``, logs every outbound request to stderr.

    Returns
    -------
    BlocklogClient
        The configured global client instance.  You normally don't need
        to store this — all module-level helpers (``decision``,
        ``approval``, ``incident``, ``replay``, ``verify``,
        ``compliance``) pick it up automatically.

    Examples
    --------
    >>> import blocklog
    >>> blocklog.init(api_key="blk_live_...")

    >>> # Environment-variable driven (CI / production)
    >>> blocklog.init()
    """
    from blocklog._global import set_client
    from blocklog.client import BlocklogClient
    from blocklog.config import BlocklogConfig

    overrides: dict = {}
    if api_key is not None:
        overrides["api_key"] = api_key
    if base_url is not None:
        overrides["base_url"] = base_url
    if signing_key is not None:
        overrides["signing_key"] = signing_key
    if timeout is not None:
        overrides["timeout"] = timeout
    if max_retries is not None:
        overrides["max_retries"] = max_retries

    config = BlocklogConfig(**overrides)

    if debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("blocklog").setLevel(logging.DEBUG)

    client = BlocklogClient(config)
    set_client(client)
    return client
