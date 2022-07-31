import abc
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