from Database.models import Signals
from sqlalchemy.orm import Session
from Libraries.logger import get_logger

logger = get_logger(__name__)


class SignalsService:
    def __init__(self, db: Session):
        self.db = db

    def save_signal(self, data: dict) -> Signals:
        existing_signal = (
            self.db.query(Signals).filter(Signals.id == data["id"]).first()
        )
        if not existing_signal:
            try:
                signal = Signals(**data)
                self.db.add(signal)
                self.db.commit()
                self.db.refresh(signal)
                logger.info(f"Signal inserted successfully: {signal.crypto_name}")
                return signal
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error inserting signal: {e}")
                raise

    def get_all_signals(self):
        return self.db.query(Signals).all()
    
    def update_signal(self, data: dict, signal_id: int) -> Signals:
        signal = self.db.query(Signals).filter(Signals.id == signal_id).first()
        if signal:
            for var, value in data.items():
                setattr(signal, var, value)
            self.db.commit()
            self.db.refresh(signal)
            return signal
        return None
    

    def delete_signal(self, signal_id: int) -> Signals:
        signal = self.db.query(Signals).filter(Signals.id == signal_id).first()
        if signal:
            self.db.delete(signal)
            self.db.commit()
            return signal
        return None
    
