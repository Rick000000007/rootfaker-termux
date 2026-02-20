class RootFakerError(Exception):
    """Base exception for RootFaker runtime."""
    pass


class ProfileNotFound(RootFakerError):
    pass


class InvalidProfileConfig(RootFakerError):
    pass


class RuntimeExecutionError(RootFakerError):
    pass
