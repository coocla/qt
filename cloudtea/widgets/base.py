#coding:utf-8
import qtawesome as qta

from PySide.QtCore import Qt, Signal, QObject
from PySide.QtGui import QFrame, QScrollArea, QHBoxLayout, QLabel, QTableWidget, \
    QDialog, QLineEdit, QPushButton


class TFrame(QFrame):
    def __init__(self, parent=None):
        super(TFrame, self).__init__(parent=parent)

    def set_theme_style(self):
        self.setStyleSheet('background: transparent;')

class TLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(TLabel, self).__init__(*args, **kwargs)

    def set_theme_style(self):
        pass

class TScrollArea(QScrollArea):
    def __init__(self, *args, **kwargs):
        super(TScrollArea, self).__init__(*args, **kwargs)

    def set_theme_style(self):
        pass

class TButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(TButton, self).__init__(*args, **kwargs)

    def set_theme_style(self):
        pass

class TLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(TLineEdit, self).__init__(parent)

    def set_theme_style(self):
        pass

class TDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(TDialog, self).__init__(*args, **kwargs)

    def set_theme_style(self):
        pass

class TObject(QObject):
    def __init__(self, parent=None):
        super(TObject, self).__init__(parent)

    def set_theme_style(self):
        pass

class TTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(TTableWidget, self).__init__(*args, **kwargs)

    def set_theme_style(self):
        pass

class TGroupHeader(TFrame):
    def __init__(self, app, title=None, parent=None):
        super(TGroupHeader, self).__init__(parent)
        self._app = app

        self._layout = QHBoxLayout()
        self.title_label = TLabel(title, self)
        self.title_label.setIndent(8)

        self.setObjectName('group_header')
        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
            }}
            #{0} QLabel {{
                font-size: 12px;
                color: {1};
            }}
        '''.format(self.objectName(),
                   theme.color5_light.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setFixedHeight(22)
        self._layout.addWidget(self.title_label)

    def set_header(self, text):
        self.title_label.setText(text)

class TGroupItem(TFrame):
    clicked = Signal()

    def __init__(self, app, name=None, parent=None):
        super(TGroupItem, self).__init__(parent)
        self._app = app

        self.is_selected=False
        self._layout = QHBoxLayout(self)
        self._flag_label = TLabel(self)
        self._img_label = TLabel(self)
        self._name_label = TLabel(name, self)

        self.setObjectName('group_item')
        self._flag_label.setObjectName('lp_groun_item_flag')
        self._flag_label.setIndent(5)
        self._img_label.setObjectName('lp_group_item_img')
        #icon = qta.icon('fa.anchor')
        #self._img_label.setText(icon)
        self._name_label.setObjectName('lp_group_item_name')

        self.set_theme_style()
        self.setup_ui()

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: transparent;
            }}
            #{1} {{
                color: transparent;
                font-size: 14px;
            }}
            #{2} {{
                color: {4};
                font-size: 14px;
            }}
            #{3} {{
                color: {4};
                font-size: 13px;
            }}
        '''.format(self.objectName(),
                   self._flag_label.objectName(),
                   self._img_label.objectName(),
                   self._name_label.objectName(),
                   theme.random_color().name(),
                   theme.color0.name())
        self.setStyleSheet(style_str)

    def setup_ui(self):
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(0)
        self.setFixedHeight(26)
        self._img_label.setFixedHeight(18)

        self._layout.addWidget(self._img_label)
        self._layout.addSpacing(2)
        self._layout.addWidget(self._name_label)

    def set_img_text(self, text):
        self._img_label.setText(text)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit()

    def set_selected(self):
        print "I am selected"