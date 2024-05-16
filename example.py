import asyncio
import logging

from connections.database import init_db
from connections.database.requests.analytic.crud import add_products
from connections.wildberries import get_data_from_zip
from connections.wildberries.api import Wildberries
import pandas as pd

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def generate_date_range(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date)
    return [date.strftime('%Y-%m-%d') for date in date_range]


async def sjrpc(wb_client):
    while True:
        try:
            logging.info('Пробую получить sjrpc токен')

            tokensjrpc = await wb_client.get_tokensjrpc()
            logging.info('sjrpc токен получен')

            return tokensjrpc
        except:
            logging.error('Ошибка: sjrpc токен не получен')
            await asyncio.sleep(1)


async def main():
    cookies = { #Скопировать из любого запроса на странице вашего ЛК (F12 - Network)
        "Request Cookies": {
            "___wbu": "db8661056",
            "__zzatw-wb": "MDA0dC0cw7FmBtyZg==I1uDZg==",
            "_wbauid": "8021056",
            "cfidsw-wb": "zR112ZySA=",
            "external-locale": "ru",
            "wb-id": "gYFijJlNjllMw",
            "wb-pid": "gYHKwHEVbwFDlRElQgN7a2TrHzi70OQ",
            "wb-sid": "03c73069e3",
            "WBTokenV3": "eyJhbGciOiJSUzI1Nun7Yhu_pXSn0d5-DMLg-",
            "wbx-validation-key": "7f6106ec091bda8",
            "x-supplier-id-external": "95fdf020a1e668"
        }
    }

    wb_client = Wildberries(cookies=cookies['Request Cookies'])
    tokensjrpc = await sjrpc(wb_client)
    logging.info('Подключил ЛК')

    for date in generate_date_range('2023-11-01', '2024-05-15'): #Нужные Вам даты
        logging.info(f'Отправляю запрос на выгрузку отчёта за {date}')
        file_id = await wb_client.download_search_phrase_report(date)

        zip = False
        while not zip:
            download_list = await wb_client.get_downloads()

            for download in download_list:
                if download['id'] == file_id:
                    if download['status'] == 'SUCCESS':
                        logging.info('Отчёт готов')
                        try:
                            zip = await wb_client.download_file(tokensjrpc, file_id)
                            logging.info('Отчёт скачен')
                        except:
                            logging.error('Отчёт не скачен, возможно jrpc токен')
                            tokensjrpc = await sjrpc(wb_client)
                            continue
                        break
                    else:
                        logging.info('Жду отчёт...')
                        await asyncio.sleep(4)

        logging.info('Открываю архив')
        analytics = await get_data_from_zip(zip, file_id, date)

        await init_db()
        logging.info(f'Сохранил в БД отчёт за {date}')
        await add_products(analytics)

        logging.info('Жду 5 секунд на всякий =)')
        await asyncio.sleep(4)

    await wb_client.close()


if __name__ == "__main__":
    asyncio.run(main())
