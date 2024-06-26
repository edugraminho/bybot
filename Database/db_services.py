from Database.models import Signals
from sqlalchemy.orm import Session


class SignalsService:
    def __init__(self, db: Session):
        self.db = db

    def save_signal(self, data: dict) -> Signals:
        db_user = Signals(**data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_signal(self, data: dict, signal_id: int) -> Signals:
        signal = self.db.query(Signals).filter(Signals.id == signal_id).first()
        if signal:
            for var, value in data.items():
                setattr(signal, var, value)
            self.db.commit()
            self.db.refresh(signal)
            return signal
        return None
