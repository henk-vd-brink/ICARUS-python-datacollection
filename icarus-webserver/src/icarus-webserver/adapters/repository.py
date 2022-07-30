import abc
from typing import Set

from ..adapters import orm
from ..domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self, model):
        self.session.add(model)
        self.seen.add(model)

class ImageSqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def get(self, uuid) -> model.Image:
        image = self.session.query(model.Image).filter_by(uuid=uuid).first()
        if image: 
            self.seen.add(image)
        return image
    
    def get_all(self):
        return self.session.query(model.Image).all()


class TransactionSqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def get(self, transaction_id):
        transaction = self.session.query(model.Transaction).filter_by(transaction_id=transaction_id).first()
        if transaction:
            self.seen.add(transaction)
        return transaction