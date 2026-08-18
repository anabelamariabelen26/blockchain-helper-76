import json

class InputValidationError(Exception):
    pass

class Processor:
    def __init__(self):
        pass

    def validate_input(self, data):
        if not isinstance(data, dict):
            raise InputValidationError("Data must be a dictionary.")
        if "amount" not in data or not isinstance(data["amount"], (int, float)):
            raise InputValidationError("'amount' is required and must be a number.")
        if "currency" not in data or not isinstance(data["currency"], str):
            raise InputValidationError("'currency' is required and must be a string.")

    def process(self, data):
        try:
            self.validate_input(data)
            # Processing logic here
            return json.dumps({"status": "success", "data": data})
        except InputValidationError as e:
            return json.dumps({"status": "error", "message": str(e)})

if __name__ == '__main__':
    processor = Processor()
    input_data = {"amount": 100, "currency": "USD"}
    result = processor.process(input_data)
    print(result)