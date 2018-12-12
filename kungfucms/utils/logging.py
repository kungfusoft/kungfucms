# PROJECT : kungfucms
# TIME : 2018/11/20 11:27
# AUTHOR : Younger Shen
# EMAIL : youngershen64@gmail.com
# CELL : 13811754531
# WECHAT : 13811754531
from datetime import datetime
from logging import FileHandler as BaseFileHandler, Handler, LogRecord
from django.utils.timezone import make_aware
from kungfucms.utils.common import get_log_file


class FileHandler(BaseFileHandler):

    def _open(self):
        self.baseFilename = get_log_file()
        return open(self.baseFilename, self.mode, encoding=self.encoding)

    def emit(self, record):
        """
        Emit a record.
        If the stream was not opened because 'delay' was specified in the
        constructor, open it before calling the superclass's emit.
        """
        if self.stream is None:
            self.stream = self._open()
        super().emit(record)
        self.stream.close()
        self.stream = None


class DBHandler(Handler):
    def emit(self, record: LogRecord):
        from kungfucms.apps.system.models import LogRecord as Record
        traceback = self.format(record)
        message = record.getMessage()
        create_at = datetime.fromtimestamp(record.created)

        kwargs = {
            'level_name': record.levelname,
            'asctime': make_aware(create_at),
            'pathname': record.pathname,
            'funcname': record.funcName,
            'lineno': record.lineno,
            'message': message,
            'traceback': traceback
        }
        Record.objects.create(**kwargs)
