from abc import ABC, abstractmethod

class BaseQueries(ABC):
    @abstractmethod
    def execute(self): # pragma: no cover
        raise NotImplementedError("Please implement in subclass")