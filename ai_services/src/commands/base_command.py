from abc import ABC, abstractmethod

class BaseCommand(ABC):
    @abstractmethod
    def execute(self): # pragma: no cover
        raise NotImplementedError("Please implement in subclass")