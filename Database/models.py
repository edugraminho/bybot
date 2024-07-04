from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Signals(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, nullable=False)
    reply_to = Column(String, nullable=True)
    date = Column(String, nullable=True)
    timestamp = Column(Integer, nullable=True)
    crypto_name = Column(String, nullable=False)
    direction = Column(String, nullable=False)
    signal_type = Column(String, nullable=False)
    status = Column(String, nullable=True)
    price_buy = Column(String, nullable=True)
    stop_price = Column(String, nullable=True)
    qty = Column(String, nullable=True)
