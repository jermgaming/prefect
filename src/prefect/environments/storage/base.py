from abc import ABCMeta, abstractmethod
import logging
from typing import TYPE_CHECKING, Any, List

import prefect
from prefect.engine.result_handlers import ResultHandler
from prefect.utilities import logging as prefect_logging

if TYPE_CHECKING:
    import prefect.core.flow


class Storage(metaclass=ABCMeta):
    """
    Base interface for Storage objects.

    Args:
        - result_handler (ResultHandler, optional): a default result handler to use for
            all flows which utilize this storage class
    """

    def __init__(self, result_handler: ResultHandler = None) -> None:
        self.result_handler = result_handler or ResultHandler()

    @property
    def labels(self) -> List[str]:
        return []

    def __repr__(self) -> str:
        return "<Storage: {}>".format(type(self).__name__)

    def get_env_runner(self, flow_location: str) -> Any:
        """
        Given a `flow_location` within this Storage object, returns something with a
        `run()` method that accepts a collection of environment variables for running the flow;
        for example, to specify an executor you would need to provide
        `{'PREFECT__ENGINE__EXECUTOR': ...}`.

        Args:
            - flow_location (str): the location of a flow within this Storage

        Returns:
            - a runner interface (something with a `run()` method for running the flow)
        """
        raise NotImplementedError()

    def get_flow(self, flow_location: str) -> "prefect.core.flow.Flow":
        """
        Given a flow_location within this Storage object, returns the underlying Flow (if possible).

        Args:
            - flow_location (str): the location of a flow within this Storage

        Returns:
            - Flow: the requested flow
        """
        raise NotImplementedError()

    @abstractmethod
    def add_flow(self, flow: "prefect.core.flow.Flow") -> str:
        """
        Method for adding a new flow to this Storage object.

        Args:
            - flow (Flow): a Prefect Flow to add

        Returns:
            - str: the location of the newly added flow in this Storage object
        """
        pass

    @property
    def name(self) -> str:
        """
        Name of the environment.  Can be overriden.
        """
        return type(self).__name__

    @property
    def logger(self) -> "logging.Logger":
        """
        Prefect logger.
        """
        return prefect_logging.get_logger(type(self).__name__)

    @abstractmethod
    def __contains__(self, obj: Any) -> bool:
        """
        Method for determining whether an object is contained within this storage.
        """
        pass

    @abstractmethod
    def build(self) -> "Storage":
        """
        Build the Storage object.

        Returns:
            - Storage: a Storage object that contains information about how and where
                each flow is stored
        """
        raise NotImplementedError()

    def serialize(self) -> dict:
        """
        Returns a serialized version of the Storage object

        Returns:
            - dict: the serialized Storage
        """
        schema = prefect.serialization.storage.StorageSchema()
        return schema.dump(self)
