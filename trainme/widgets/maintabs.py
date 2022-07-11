from PyQt5.QtWidgets import QTabWidget

from .labeling.labeling_wrapper import LabelingWrapper
from .workspace.workspace_wrapper import WorkspaceWrapper


class MainTabsWidget(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tabs = []

        self.labeling_tab = LabelingWrapper(self)
        self.tabs.append(self.labeling_tab)
        self.addTab(self.labeling_tab, "Labeling")

        self.workspace_tab = WorkspaceWrapper(self)
        self.tabs.append(self.workspace_tab)
        self.addTab(self.workspace_tab, "Workspace")

        self.currentChanged.connect(self.on_change)

    def on_change(self, i):
        # Show/hide menu
        if isinstance(self.tabs[i], LabelingWrapper):
            self.parent.menuBar().show()
        else:
            self.parent.menuBar().hide()
