from abc import ABC, abstractmethod


class StorageInterface(ABC):
    """
    Interface that all storage classes should implement
    """
    @abstractmethod
    def get_file(self, city):
        '''
        Returns files from storage which name starts with city
        '''
        pass

    @abstractmethod
    def upload(self, file_name):
        '''
        Uploads file to storage
        '''
        pass