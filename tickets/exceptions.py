from rest_framework.exceptions import APIException

class CannotPerformOperation(APIException):
    status_code = 423
    default_detail = 'Operation cannot be perform because the resource has been publish, and cannot be update.'
    default_code = 'object_publish'