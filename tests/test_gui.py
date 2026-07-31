from __future__ import annotations

import inspect

from PySide6.QtWidgets import QMainWindow, QWidget

from bubblecraps.gui.animations import AnimationManager
from bubblecraps.gui.main_window import MainWindow
from bubblecraps.gui.styles import ApplicationStyles
from bubblecraps.gui.table_widget import TableWidget


def test_gui_shell_exposes_the_pag_widget_contract() -> None:
    assert issubclass(MainWindow, QMainWindow)
    assert list(inspect.signature(MainWindow).parameters) == ["controller"]
    assert issubclass(TableWidget, QWidget)
    assert AnimationManager.__doc__ is not None
    assert ApplicationStyles.__doc__ is not None
