from PyQt5 import QtCore, QtWidgets


class ToolBar(QtWidgets.QToolBar):
    def __init__(self, title):
        super(ToolBar, self).__init__(title)
        layout = self.layout()
        margin = (0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setContentsMargins(*margin)
        self.setContentsMargins(*margin)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

    def add_action(self, action):
        if isinstance(action, QtWidgets.QWidgetAction):
            return super(ToolBar, self).addAction(action)
        btn = QtWidgets.QToolButton()
        btn.setDefaultAction(action)
        btn.setToolButtonStyle(self.toolButtonStyle())
        self.addWidget(btn)

        # Center alignment
        for i in range(self.layout().count()):
            if isinstance(
                self.layout().itemAt(i).widget(), QtWidgets.QToolButton
            ):
                self.layout().itemAt(i).setAlignment(QtCore.Qt.AlignCenter)

        return True