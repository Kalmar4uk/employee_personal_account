from rest_framework import status
from rest_framework.exceptions import APIException


class NotShiftForCreateDowntime(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = None
    default_code = "error"
