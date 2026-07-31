"""Define the main application window shell."""

from __future__ import annotations

from PySide6.QtWidgets import QMainWindow

from bubblecraps.controller.session_controller import SessionController
from bubblecraps.gui.table_widget import TableWidget


class MainWindow(QMainWindow):
    """Provide the future primary Bubble Craps game window."""

    def __init__(self, controller: SessionController) -> None:
        """Create the minimal window shell associated with a controller."""
        super().__init__()
        self._controller = controller
        self.setWindowTitle("Bubble Craps")
        self.setCentralWidget(TableWidget())
        self.statusBar()
