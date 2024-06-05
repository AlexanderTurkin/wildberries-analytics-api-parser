from sqlalchemy import Column, Integer, String, Date, DECIMAL, DateTime
from datetime import datetime
from connections.database.models import Base


class Analytic(Base):
    __tablename__ = 'analytics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String(255), nullable=True)
    Period_Start = Column(Date, nullable=True)
    Period_End = Column(Date, nullable=True)
    SKU = Column(String(255), nullable=True)
    Item = Column(String(255), nullable=True)
    Title = Column(String(255), nullable=True)
    Category = Column(String(255), nullable=True)
    Brand = Column(String(255), nullable=True)
    Card_Rating = Column(DECIMAL(10, 0), nullable=True)
    Search_Query = Column(String(255), nullable=True)
    Frequency_Current = Column(Integer, nullable=True)
    Frequency_Prev = Column(Integer, nullable=True)
    Visibility_Current = Column(DECIMAL(5, 2), nullable=True)
    Visibility_Prev = Column(DECIMAL(5, 2), nullable=True)
    Avg_Position_Current = Column(DECIMAL(5, 2), nullable=True)
    Avg_Position_Prev = Column(DECIMAL(5, 2), nullable=True)
    Median_Position_Current = Column(DECIMAL(5, 2), nullable=True)
    Median_Position_Prev = Column(DECIMAL(5, 2), nullable=True)
    Card_Clicks_Current = Column(Integer, nullable=True)
    Card_Clicks_Prev = Column(Integer, nullable=True)
    Card_Clicks_Better_Than_Percent = Column(DECIMAL(5, 2), nullable=True)
    Added_to_Cart_Current = Column(Integer, nullable=True)
    Added_to_Cart_Prev = Column(Integer, nullable=True)
    Added_to_Cart_Better_Than_Percent = Column(DECIMAL(5, 2), nullable=True)
    Cart_Conversion_Current = Column(DECIMAL(5, 2), nullable=True)
    Cart_Conversion_Prev = Column(DECIMAL(5, 2), nullable=True)
    Ordered_Current = Column(Integer, nullable=True)
    Ordered_Prev = Column(Integer, nullable=True)
    Orders_Better_Than_Percent = Column(DECIMAL(5, 2), nullable=True)
    Order_Conversion_Current = Column(DECIMAL(5, 2), nullable=True)
    Order_Conversion_Prev = Column(DECIMAL(5, 2), nullable=True)
    Min_Price_Discounted = Column(DECIMAL(10, 2), nullable=True)
    Max_Price_Discounted = Column(DECIMAL(10, 2), nullable=True)
    Date_Added = Column(DateTime, default=datetime.utcnow, nullable=True)


COLUMN_MAPPING = {
    "Артикул продавца": "SKU",
    "Номенклатура": "Item",
    "Название": "Title",
    "Категория": "Category",
    "Бренд": "Brand",
    "Рейтинг карточки": "Card_Rating",
    "Поисковый запрос": "Search_Query",
    "Частота, шт": "Frequency_Current",
    "Частота, шт (предыдущий период)": "Frequency_Prev",
    "Видимость, %": "Visibility_Current",
    "Видимость, % (предыдущий период)": "Visibility_Prev",
    "Средняя позиция": "Avg_Position_Current",
    "Средняя позиция (предыдущий период)": "Avg_Position_Prev",
    "Медианная позиция": "Median_Position_Current",
    "Медианная позиция (предыдущий период)": "Median_Position_Prev",
    "Переходы в карточку": "Card_Clicks_Current",
    "Переходы в карточку (предыдущий период)": "Card_Clicks_Prev",
    "Переходы в карточку лучше, чем у n% карточек конкурентов, %": "Card_Clicks_Better_Than_Percent",
    "Положили в корзину": "Added_to_Cart_Current",
    "Положили в корзину (предыдущий период)": "Added_to_Cart_Prev",
    "Положили в корзину лучше, чем n% карточек конкурентов, %": "Added_to_Cart_Better_Than_Percent",
    "Конверсия в корзину, %": "Cart_Conversion_Current",
    "Конверсия в корзину, % (предыдущий период)": "Cart_Conversion_Prev",
    "Заказали, шт": "Ordered_Current",
    "Заказали, шт (предыдущий период)": "Ordered_Prev",
    "Заказы лучше, чем n% карточек конкурентов, %": "Orders_Better_Than_Percent",
    "Конверсия в заказ, %": "Order_Conversion_Current",
    "Конверсия в заказ, % (предыдущий период)": "Order_Conversion_Prev",
    "Минимальная цена со скидкой (по размерам)": "Min_Price_Discounted",
    "Максимальная цена со скидкой (по размерам)": "Max_Price_Discounted"
}
