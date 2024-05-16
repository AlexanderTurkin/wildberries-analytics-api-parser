import asyncio
import io
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pandas as pd

from connections.database.models.analytics import Analytic


async def get_data_from_zip(binary_data, file_id: str, request_date: str):
    executor = ThreadPoolExecutor(max_workers=2)

    zip_buffer = io.BytesIO(binary_data)

    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        for file_name in zip_file.namelist():
            if file_name.endswith('.xlsx'):
                file_data = zip_file.read(file_name)
                xlsx_data = io.BytesIO(file_data)

                df = await asyncio.get_event_loop().run_in_executor(
                    executor,
                    pd.read_excel,
                    xlsx_data,
                    2
                )

                analytics = []
                for _, row in df.iterrows():
                    if _ == 0:
                        continue

                    analytic = Analytic(
                        file_id=file_id,
                        Period_Start=datetime.strptime(request_date, "%Y-%m-%d").date(),
                        Period_End=datetime.strptime(request_date, "%Y-%m-%d").date(),
                        SKU=row.iloc[0],
                        Item=row.iloc[1],
                        Title=row.iloc[2],
                        Category=row.iloc[3],
                        Brand=row.iloc[4],
                        Card_Rating=row.iloc[5],
                        Search_Query=row.iloc[6],
                        Frequency_Current=row.iloc[7],
                        Frequency_Prev=row.iloc[8],
                        Visibility_Current=row.iloc[9],
                        Visibility_Prev=row.iloc[10],
                        Avg_Position_Current=row.iloc[11],
                        Avg_Position_Prev=row.iloc[12],
                        Median_Position_Current=row.iloc[13],
                        Median_Position_Prev=row.iloc[14],
                        Card_Clicks_Current=row.iloc[15],
                        Card_Clicks_Prev=row.iloc[16],
                        Added_to_Cart_Current=row.iloc[17],
                        Added_to_Cart_Prev=row.iloc[18],
                        Cart_Conversion_Current=row.iloc[19],
                        Cart_Conversion_Prev=row.iloc[20],
                        Ordered_Current=row.iloc[21],
                        Ordered_Prev=row.iloc[22],
                        Order_Conversion_Current=row.iloc[23],
                        Order_Conversion_Prev=row.iloc[24],
                        Min_Price_Discounted=row.iloc[25],
                        Max_Price_Discounted=row.iloc[26],
                        Date_Added=datetime.utcnow()
                    )
                    analytics.append(analytic)

                return analytics
