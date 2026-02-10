from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from aiohttp import ClientResponse, ContentTypeError

from codercore.lib.http.exceptions import UnexpectedThirdPartyResponseError


@asynccontextmanager
async def verify_third_party_response(response: ClientResponse) -> AsyncIterator[None]:
    """Context manager that raises UnexpectedThirdPartyResponseError on failure."""
    try:
        yield
    except (ValueError, KeyError, ContentTypeError):
        raise UnexpectedThirdPartyResponseError(response, await response.text())
