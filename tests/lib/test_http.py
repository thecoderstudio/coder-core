import pytest
from aiohttp import ContentTypeError

from codercore.lib.http import (
    UnexpectedThirdPartyResponseError,
    verify_third_party_response,
)


def test_unexpected_third_party_response_error(mocker):
    request_info_mock = mocker.MagicMock()
    request_info_mock.method = "POST"
    request_info_mock.url = "http://localhost"
    response_mock = mocker.MagicMock()
    response_mock.request_info = request_info_mock
    response_mock.status = 400
    response_text = "Sample text"

    exc = UnexpectedThirdPartyResponseError(response_mock, response_text)
    assert str(exc) == (
        f"Unexpected response for {request_info_mock.method} "
        + f"{request_info_mock.url}: {response_mock.status} - "
        + response_text
    )


@pytest.mark.parametrize("exception", (KeyError, ValueError, ContentTypeError))
async def test_verify_third_party_response_thrown(exception, mocker):
    response_mock = mocker.AsyncMock()
    with pytest.raises(UnexpectedThirdPartyResponseError) as e:
        async with verify_third_party_response(response_mock):
            if exception is ContentTypeError:
                raise ContentTypeError(mocker.MagicMock(), mocker.MagicMock())
            raise exception
    assert e.value.response == response_mock


async def test_verify_third_party_response_success(mocker):
    response_mock = mocker.MagicMock()
    async with verify_third_party_response(response_mock):
        pass
