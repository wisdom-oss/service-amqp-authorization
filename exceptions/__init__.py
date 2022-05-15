import http
import typing


class ServiceException(Exception):
    """ """

    def __init__(
        self,
        error_code: str,
        error_name: typing.Optional[str] = None,
        error_description: typing.Optional[str] = None,
        status_code: http.HTTPStatus = http.HTTPStatus.BAD_REQUEST,
    ):
        """Create a new Service Exception

        :param short_error: Short error description (e.g. USER_NOT_FOUND)
        :param error_description: Textual description of the error (may point to the documentation)
        :param status_code: HTTP Status code which shall be sent back by the error handler
        :param optional_data: Any optional data which shall be sent witch the error handler
        """
        super().__init__()
        self.error_code = error_code
        self.error_name = error_name
        self.error_description = error_description
        self.http_code = status_code
