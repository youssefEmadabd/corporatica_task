from flask import jsonify

class APIException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_response(self):
        """Returns a JSON response with error details"""
        response = jsonify({"error": self.message})
        response.status_code = self.status_code
        return response