def build_headers(
    api_key: str = "",
    *,
    access_token: str = "",
    extra: dict[str, str] | None = None,
    skip_auth: bool = False,
) -> dict[str, str]:
    headers = {
        "Content-Type": "application/json",
    }
    if not skip_auth:
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        elif api_key:
            headers["X-API-Key"] = api_key
    if extra:
        headers.update(extra)
    return headers
