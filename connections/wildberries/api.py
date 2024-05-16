import uuid
from typing import Mapping, Optional, List

from connections.wildberries.base import BaseClient


class Wildberries(BaseClient):
    def __init__(self, cookies: Mapping[str, str], **kwargs):
        self.cookies = cookies
        self.base_url = "https://seller-content.wildberries.ru"
        super().__init__(base_url=self.base_url)

    async def download_search_phrase_report(self, date: str = '2023-05-16', brand: Optional[List[str]] = None,
                                            **kwargs) -> str:
        if brand is None:
            brand = ['Fase-OFF']

        file_id = str(uuid.uuid4())

        response = await self._make_request(
            endpoint='/ns/analytics-api/content-analytics/api/v1/file-manager/download',
            method='post',
            json={
                "id": file_id,
                "reportType": "SEARCH_PHRASE_REPORT",
                "userReportName": "",
                "params":
                    {
                        "startDate": date,
                        "endDate": date,
                        "brands": brand,
                        "subjects": [],
                        "tags": [],
                        "nms": [],
                        "vendorCodes": [],
                        "orderBy": {"field": "openCard", "mode": "desc"},
                        "phrasesLimit": 20
                    }
            },
            cookies=self.cookies
        )

        if response[0] == 200:
            return file_id
        else:
            raise Exception('Wildberries could not download search phrases report')

    async def get_downloads(self, report_type: str = 'SEARCH_PHRASE_REPORT', **kwargs) -> List[str]:
        response = await self._make_request(
            endpoint='/ns/analytics-api/content-analytics/api/v1/file-manager/downloads',
            params={
                'report_types': report_type
            },
            method='get',
            cookies=self.cookies
        )

        if response[0] == 200:
            return response[1]['data']['downloads']
        else:
            raise Exception('Wildberries could not downloads list')

    async def get_tokensjrpc(self, **kwargs) -> str:
        response = await self._make_request(
            endpoint='/ns/suppliers-auth-tokens/suppliers-portal-core/api/v1/tokensjrpc',
            method='post',
            json={
                "method": "generateToken",
                "params": {"team": "content-analytics"},
                "jsonrpc": "2.0",
                "id": "json-rpc_19"
            },
            headers={
                "TE": "trailers"
            },
            cookies=self.cookies
        )

        if response[0] == 200:
            try:
                return response[1]['result']['token']
            except:
                raise Exception('Try again now')
        else:
            raise Exception('Wildberries could not tokensjrpc')

    async def download_file(self, tokensjrpc: str, file_id: str, **kwargs) -> List[str]:
        response = await self._make_request(
            base_url_override='https://downloads-content-analytics.wildberries.ru',
            endpoint='/api/v1/file-manager/download/' + file_id,
            headers={
                'x-download-token': tokensjrpc
            },
            method='get',
            response_type='file',
            cookies=self.cookies
        )

        if response[0] == 200:
            return response[1]
        else:
            raise Exception('File download could not download')
