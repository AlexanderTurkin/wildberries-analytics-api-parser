import io
import zipfile
from datetime import datetime

import pandas as pd

from connections.database.models.analytics import Analytic, COLUMN_MAPPING


async def get_data_from_zip(binary_data, file_id: str, request_date: str):
    zip_buffer = io.BytesIO(binary_data)

    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        for file_name in zip_file.namelist():
            if file_name.endswith('.xlsx'):
                file_data = zip_file.read(file_name)
                xlsx_data = io.BytesIO(file_data)

                df = pd.read_excel(xlsx_data, sheet_name=2, header=1)

                for column in df.columns:
                    if column not in COLUMN_MAPPING:
                        raise ValueError(f"Столбец {column} не соответствует ни одному столбцу в модели данных.")

                df.rename(columns=COLUMN_MAPPING, inplace=True)

                analytics = []
                for _, row in df.iterrows():
                    analytic = Analytic(
                        file_id=file_id,
                        Period_Start=datetime.strptime(request_date, "%Y-%m-%d").date(),
                        Period_End=datetime.strptime(request_date, "%Y-%m-%d").date(),
                        SKU=row.get("SKU"),
                        Item=row.get("Item"),
                        Title=row.get("Title"),
                        Category=row.get("Category"),
                        Brand=row.get("Brand"),
                        Card_Rating=row.get("Card_Rating"),
                        Search_Query=row.get("Search_Query"),
                        Frequency_Current=row.get("Frequency_Current"),
                        Frequency_Prev=row.get("Frequency_Prev"),
                        Visibility_Current=row.get("Visibility_Current"),
                        Visibility_Prev=row.get("Visibility_Prev"),
                        Avg_Position_Current=row.get("Avg_Position_Current"),
                        Avg_Position_Prev=row.get("Avg_Position_Prev"),
                        Median_Position_Current=row.get("Median_Position_Current"),
                        Median_Position_Prev=row.get("Median_Position_Prev"),
                        Card_Clicks_Current=row.get("Card_Clicks_Current"),
                        Card_Clicks_Prev=row.get("Card_Clicks_Prev"),
                        Card_Clicks_Better_Than_Percent=row.get("Card_Clicks_Better_Than_Percent"),
                        Added_to_Cart_Current=row.get("Added_to_Cart_Current"),
                        Added_to_Cart_Prev=row.get("Added_to_Cart_Prev"),
                        Added_to_Cart_Better_Than_Percent=row.get("Added_to_Cart_Better_Than_Percent"),
                        Cart_Conversion_Current=row.get("Cart_Conversion_Current"),
                        Cart_Conversion_Prev=row.get("Cart_Conversion_Prev"),
                        Ordered_Current=row.get("Ordered_Current"),
                        Ordered_Prev=row.get("Ordered_Prev"),
                        Orders_Better_Than_Percent=row.get("Orders_Better_Than_Percent"),
                        Order_Conversion_Current=row.get("Order_Conversion_Current"),
                        Order_Conversion_Prev=row.get("Order_Conversion_Prev"),
                        Min_Price_Discounted=row.get("Min_Price_Discounted"),
                        Max_Price_Discounted=row.get("Max_Price_Discounted"),
                        Date_Added=datetime.utcnow()
                    )
                    analytics.append(analytic)

                return analytics
