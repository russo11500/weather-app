from abc import ABC, abstractmethod


class DBInterface(ABC):
    """
    Interface that all DB classes should implement
    """
    @abstractmethod
    def save_data(self, file_name):
        '''
        Uploads file to storage
        '''
        pass
