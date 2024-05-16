from sqlalchemy import Column, Integer, String, Date, DECIMAL, DateTime
from datetime import datetime

from connections.database.models import Base


class Analytic(Base):
    __tablename__ = 'analytics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String(255), nullable=False)
    Period_Start = Column(Date, nullable=False)
    Period_End = Column(Date, nullable=False)
    SKU = Column(String(255), nullable=False)
    Item = Column(String(255), nullable=False)
    Title = Column(String(255), nullable=False)
    Category = Column(String(255), nullable=False)
    Brand = Column(String(255), nullable=False)
    Card_Rating = Column(DECIMAL(10, 0), nullable=False)
    Search_Query = Column(String(255), nullable=False)
    Frequency_Current = Column(Integer, nullable=False)
    Frequency_Prev = Column(Integer, nullable=False)
    Visibility_Current = Column(DECIMAL(5, 2), nullable=False)
    Visibility_Prev = Column(DECIMAL(5, 2), nullable=False)
    Avg_Position_Current = Column(DECIMAL(5, 2), nullable=False)
    Avg_Position_Prev = Column(DECIMAL(5, 2), nullable=False)
    Median_Position_Current = Column(DECIMAL(5, 2), nullable=False)
    Median_Position_Prev = Column(DECIMAL(5, 2), nullable=False)
    Card_Clicks_Current = Column(Integer, nullable=False)
    Card_Clicks_Prev = Column(Integer, nullable=False)
    Added_to_Cart_Current = Column(Integer, nullable=False)
    Added_to_Cart_Prev = Column(Integer, nullable=False)
    Cart_Conversion_Current = Column(DECIMAL(5, 2), nullable=False)
    Cart_Conversion_Prev = Column(DECIMAL(5, 2), nullable=False)
    Ordered_Current = Column(Integer, nullable=False)
    Ordered_Prev = Column(Integer, nullable=False)
    Order_Conversion_Current = Column(DECIMAL(5, 2), nullable=False)
    Order_Conversion_Prev = Column(DECIMAL(5, 2), nullable=False)
    Min_Price_Discounted = Column(DECIMAL(10, 2), nullable=False)
    Max_Price_Discounted = Column(DECIMAL(10, 2), nullable=False)
    Date_Added = Column(DateTime, default=datetime.utcnow, nullable=False)
