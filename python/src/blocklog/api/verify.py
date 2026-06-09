"""
blocklog.api.verify
~~~~~~~~~~~~~~~~~~~
Layer 2 client for cryptographic verification.

Available via ``client.verify.*``.

Backend endpoints
-----------------
- GET  /api/v1/verify/log/{log_id}
- GET  /api/v1/verify/batch/{batch_id}
- GET  /api/v1/decisions/{id}/verify
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from blocklog.client import BlocklogClient


class VerifyClient:
    """Cryptographically verify logs, batches, and decisions.

    Every item recorded by Blocklog is anchored to a blockchain via a
    Merkle tree.  These methods let you prove that a specific log entry
    or batch has not been tampered with since it was anchored.

    Accessed as ``client.verify``.

    Examples
    --------
    >>> result = client.verify.log("log-uuid-here")
    >>> print(result["status"])   # "verified"
    >>> print(result["merkle_proof"])

    >>> result = client.verify.decision("dec-uuid-here")
    >>> print(result["status"])   # "verified"
    """

    def __init__(self, client: "BlocklogClient") -> None:
        self._client = client

    def log(self, log_id: str) -> dict[str, Any]:
        """Verify a single log entry against its Merkle proof.

        Parameters
        ----------
        log_id:
            UUID of the log entry to verify.

        Returns
        -------
        dict
            Keys: ``status``, ``merkle_proof``, ``batch_anchor``,
            ``time_attestation``, ``details``.

        Raises
        ------
        httpx.HTTPStatusError
            If the log is not found or verification fails.
        """
        return self._client.retry.run(
            lambda: self._client.transport.request("GET", f"/verify/log/{log_id}")
        )

    def batch(self, batch_id: str) -> dict[str, Any]:
        """Verify an entire batch against its blockchain anchor.

        Parameters
        ----------
        batch_id:
            ID of the batch to verify.

        Returns
        -------
        dict
            Keys: ``status``, ``anchor_tx``, ``timestamp``,
            ``time_attestation``, ``details``.
        """
        return self._client.retry.run(
            lambda: self._client.transport.request("GET", f"/verify/batch/{batch_id}")
        )

    def decision(self, decision_id: str) -> dict[str, Any]:
        """Verify all evidence attached to a decision.

        Parameters
        ----------
        decision_id:
            UUID of the decision to verify.

        Returns
        -------
        dict
            Verification summary including Merkle and blockchain evidence.
        """
        return self._client.retry.run(
            lambda: self._client.transport.request("GET", f"/decisions/{decision_id}/verify")
        )
