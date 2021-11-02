from abc import ABC, abstractmethod

from sqlalchemy.orm import session

from allocation.domain.model import batch


class AbstractRepository(ABC):

    @abstractmethod
    def  add_batch(self, batch:batch.Batch):
        raise NotImplementedError

    @abstractmethod
    def get_batch(self, reference)->  batch.Batch:
        raise NotImplementedError

class SqlAchemyRepository(AbstractRepository):

    def __init__(self, session:session):
        self.session = session

    def add_batch(self, batch:batch.Batch):
        self.session.add(batch)

    def get_batch(self, reference) ->  batch.Batch:
        self.session.query(batch.Batch).filter_by(reference=reference).one()