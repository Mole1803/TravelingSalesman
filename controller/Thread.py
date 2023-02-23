from PySide6 import QtCore
from PySide6.QtCore import QObject, QThread

class CWorker(QObject):
    return_signal = QtCore.Signal(object)

    def __init__(self,parent=None, func=None, *args, **kwargs):
        super(CWorker, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs


    def run(self):
        result = None
        if self.args is not None:
            if self.kwargs is not None:
                result = self.func(*self.args, **self.kwargs)
            else:
                result = self.func(*self.args)
        if self.kwargs is not None:
            result = self.func(**self.kwargs)
        self.return_signal.emit(result)


class CThread(QThread):
    return_signal = QtCore.Signal(object)
    def __init__(self, func=None, *args, **kwargs):
        super(CThread, self).__init__()

        self.worker = CWorker(func=func, *args, **kwargs)
        self.worker.return_signal.connect(self.result_signal)



    def run(self):
        self.worker.run()

    def result_signal(self, return_value):
        self.return_signal.emit(return_value)
