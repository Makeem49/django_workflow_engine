from rest_framework.exceptions import APIException

class CannotPerformOperation(APIException):
    """Exceptions to prevent user to update the target resource when it has been publsih"""
    status_code = 423
    default_detail = 'Operation cannot be perform because the resource has been publish, and cannot be update.'
    default_code = 'object_publish'


class MissingData(APIException):
    status_code = 400
    default_detail = 'Missing data, either title or body of the request is missing when ticket is excalated.'
    default_code = 'object_publish'