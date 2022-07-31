import abc
from ..domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.session = None
        self.seen = set()

    def add(self, obj):
        self.session.add(obj)
        self.seen.add(obj)


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
