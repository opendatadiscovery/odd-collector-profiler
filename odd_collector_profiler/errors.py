class InvalidConfigError(Exception):
    ...


class MissedRegisterFunction(Exception):
    def __init__(self, module_name: str) -> None:
        super().__init__(
            f"Module {module_name} must have register_profiler function",
        )
