from msilib.schema import Error
from PyQt5.QtWidgets import QErrorMessage

class ErrorDialog(QErrorMessage):
    def alert(self, message):
        self.showMessage(message)

# This doesn't work as it runs before main, need to figure out an elegant 'global' error dialog TODO
#ERRROR_DIALOG = ErrorDialog()