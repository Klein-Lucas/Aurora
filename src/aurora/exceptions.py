class AuroraError (Exception):
    pass

class TaskNotFoundError (AuroraError):
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task '{task_id}' not found")

class MissingRequiredFieldError (AuroraError):
    def __init__(self, field_names: list[str]):
        self.field_names = field_names
        fields = ", ".join(field_names)
        super().__init__(f"Required fields missing: {fields}")

class JSONNotFoundError(AuroraError):
    def __init__(self):
        super().__init__("JSON file not found")