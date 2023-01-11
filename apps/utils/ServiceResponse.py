class ServiceResponse:
    success = True
    errors = {}

    def __init__(self):
        self.data = {}

    def addError(self, key, error):
        self.errors.setdefault(key, error)
        self.success = False

    def addData(self, data):
        self.data.setdefault("data", data)

    def getResult(self):
        self.data.setdefault("errors", self.errors)
        self.data.setdefault("success", self.success)
        return self.data