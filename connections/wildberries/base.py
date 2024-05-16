import asyncio
import logging
import ssl
from typing import Any, Union

import backoff
from aiohttp import ClientError, ClientSession, TCPConnector, FormData
from ujson import dumps, loads
from collections.abc import Mapping
from fake_useragent import UserAgent


class BaseClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._session: ClientSession | None = None
        self.log = logging.getLogger(self.__class__.__name__)
        self.ua = UserAgent()

    async def _get_session(self) -> ClientSession:
        if self._session is None:
            ssl_context = ssl.SSLContext()
            connector = TCPConnector(ssl_context=ssl_context)
            self._session = ClientSession(
                connector=connector,
                json_serialize=dumps,
            )
        return self._session

    @backoff.on_exception(
        backoff.expo,
        ClientError,
        max_time=3,
    )
    async def _make_request(
            self,
            method: str,
            endpoint: str,
            params: Mapping[str, str] | None = None,
            json: Mapping[str, Any] | None = None,
            headers: Mapping[str, str] | None = None,
            data: FormData | None = None,
            cookies: Mapping[str, str] | None = None,
            base_url_override: str | None = None,
            response_type: str = 'json'
    ) -> Union[tuple[int, dict[str, Any]], tuple[int, bytes]]:
        session = await self._get_session()
        full_url = (base_url_override or self._base_url) + endpoint

        # Добавление заголовков по умолчанию, если они не были переданы
        default_headers = {
            'User-Agent': self.ua.random
        }
        if headers:
            default_headers.update(headers)

        self.log.debug(
            "Making request %r %r with json %r, params %r and cookies %r",
            method,
            full_url,
            json,
            params,
            cookies
        )
        async with session.request(
                method, full_url, params=params, json=json, headers=default_headers, data=data, cookies=cookies
        ) as response:
            status = response.status
            if status != 200:
                s = await response.text()
                print(response)
                raise ClientError(f"Got status {status} for {method} {full_url}: {s}")

            if response_type == 'json':
                try:
                    result = await response.json(loads=loads)
                except Exception as e:
                    self.log.exception(e)
                    self.log.info(f"{await response.text()}")
                    result = {}
            elif response_type == 'file':
                result = await response.read()  # Считывание ответа как бинарных данных

        self.log.debug(
            "Got response %r %r with status %r and content type %r",
            method,
            full_url,
            status,
            response_type,
        )
        return status, result

    async def close(self) -> None:
        """Graceful session close."""
        if not self._session:
            self.log.debug("There's no session to close.")
            return

        if self._session.closed:
            self.log.debug("Session already closed.")
            return

        await self._session.close()
        self.log.debug("Session successfully closed.")

        await asyncio.sleep(0.25)
