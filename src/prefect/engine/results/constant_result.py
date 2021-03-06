from typing import Any
from prefect.engine.result import Result


class ConstantResult(Result):
    """
    Hook for storing and retrieving constant Python objects. Only intended to be used
    internally.  The "backend" in this instance is the class instance itself.

    Args:
        - value (Any): the underlying value this Result should represent
    """

    def __init__(self, value: Any = None, **kwargs: Any) -> None:
        self.value = value
        super().__init__(value=value, **kwargs)

    def read(self, filepath: str) -> Result:
        """
        Returns the underlying value regardless of the argument passed.

        Args:
            - filepath (str): an unused argument
        """
        return self

    def write(self, value: Any, **kwargs: Any) -> Result:
        """
        Returns the repr of the underlying value, purely for convenience.

        Args:
            - value (Any): unused, for interface compatibility
            - **kwargs (optional): unused, for interface compatibility

        Raises:
            ValueError: ConstantResults cannot be written to
        """
        raise ValueError("Cannot write values to `ConstantResult` types.")

    def exists(self, filepath: str) -> bool:
        """
        As all Python objects are valid constants, always returns `True`.

        Args:
             - filepath (str): for interface compatibility

        Returns:
            - bool: True, confirming the constant exists.
        """
        return True
