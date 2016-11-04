#coding:utf-8
import random

from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter, QFontMetrics

from cloudtea.widgets import base


class TipsManager(object):
    tips = [
        u'您可以自定义主题哦',
    ]
    def __init__(self, app):
        self._app = app

    def show_random_tip(self):
        tip = random.choice(self.tips)
        self._app.message(u'小提示: %s' % tip)

class MessageLabel(base.TLabel):
    def __init__(self, app, parent=None):
        super(MessageLabel, self).__init__(parent)
        self._app = app

        self.setObjectName('message_label')
        self._interval = 3
        self.timer = QTimer()
        self.queue = []
        self.hide()

        self.timer.timeout.connect(self.access_message_queue)

    @property
    def common_style(self):
        style_str = '''
            #{0} {{
                padding-left: 3px;
                padding-right: 5px;
            }}
        '''.format(self.objectName())
        return style_str

    def _set_error_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.color1_light.name(),
                   theme.color7_light.name())
        self.setStyleSheet(style_str + self.common_style)

    def _set_normal_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
                color: {2};
            }}
        '''.format(self.objectName(),
                   theme.color6_light.name(),
                   theme.color7.name())
        self.setStyleSheet(style_str + self.common_style)

    def show_message(self, text, error=False):
        if self.isVisible():
            self.queue.append({'error': error, 'message': text})
            self._interval = 1.5
            return
        if error:
            self._set_error_style()
        else:
            self._set_normal_style()
        self.setText(str(len(self.queue)) + ': ' + text)
        self.show()
        self.timer.start(self._interval * 1000)

    def access_message_queue(self):
        self.hide()
        if self.queue:
            m = self.queue.pop(0)
            self.show_message(m['message'], m['error'])
        else:
            self._interval = 3

class NetworkStatus(base.TLabel):
    def __init__(self, app, text=None, parent=None):
        super(NetworkStatus, self).__init__(text, parent)
        self._app = app

        self.setToolTip(u'这里显示的是网络状况')
        self.setObjectName('network_status_label')
        self.set_theme_style()
        self._progress = 100
        self._show_progress = False
        self.set_state(1)

    def paintEvent(self, event):
        if self._show_progress:
            if self._show_progress:
                p_bg_color = self._app.theme_manager.current_theme.color0
                painter.fillRect(self.rect(), p_bg_color)
                bg_color = self._app.theme_manager.current_theme.color3
                rect = self.rect()
                percent = self._progress * 1.0 / 100
                rect.setWidth(int(rect.width() * percent)) 
                painter.fillRect(rect, bg_color) 
                painter.drawText(self.rect(), Qt.AlignVCenter | Qt.AlignHCenter, 
                    str(self._progress) + '%') 
                self._show_progress = False 
            else: 
                super().paintEvent(event)

    @property
    def common_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
                color: {2};
                padding-left: 5px;
                padding-right: 5px;
                font-size: 14px;
                font-weight: bold;
            }}
        '''.format(self.objectName(),
                   theme.color3.name(),
                   theme.background.name())
        return style_str

    def set_theme_style(self):
        self.setStyleSheet(self.common_style)

    def _set_error_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
            }}
        '''.format(self.objectName(),
                   theme.color5.name())
        self.setStyleSheet(self.common_style + style_str)

    def _set_normal_style(self):
        self.setStyleSheet(self.common_style)

    def set_state(self, state):
        if state == 0:
            self._set_error_style()
            self.setText('✕')
        elif state == 1:
            self._set_normal_style()
            self.setText('✓')

    def show_progress(self, progress):
        self._progress = progress
        self._show_progress = True
        if self._progress == 100:
            self._show_progress = False
        self.update()

class ThemeComboBox(base.TComboBox):
    clicked = pyqtSignal()
    signal_change_theme = pyqtSignal([str])

    def __init__(self, app, parent=None):
        super(ThemeComboBox, self).__init__(parent)
        self._app = app

        self.setObjectName('theme_switch_btn')
        self.setEditable(False)
        self.maximum_width = 150
        self.set_theme_style()
        self.setFrame(False)
        self.current_theme = self._app.theme_manager.current_theme.name
        self.themes = [self.current_theme]
        self.set_themes(self.themes)

        self.currentIndexChanged.connect(self.on_index_changed)

    def set_theme_style(self):
        theme = self._app.theme_manager.current_theme
        style_str = '''
            #{0} {{
                background: {1};
                color: {2};
                border: 0px;
                padding: 0px 4px;
                border-radius: 0px;
            }}
            #{0}::drop-down {{
                width: 0px;
                border: 0px;
            }}
            #{0} QAbstractItemView {{
                border: 0px;
                min-width: 200px;
            }}
        '''.format(self.objectName(),
                   theme.color4.name(),
                   theme.background.name(),
                   theme.foreground.name())
        self.setStyleSheet(style_str)

    @pyqtSlot(int)
    def on_index_changed(self, index):
        if index < 0 or not self.themes:
            return
        metrics = QFontMetrics(self.font())
        if self.themes[index] == self.current_theme:
            return
        self.current_theme = self.themes[index]
        name = '❀ ' + self.themes[index]
        width = metrics.width(name)
        if width < self.maximum_width:
            self.setFixedWidth(width + 10)
            self.setItemText(index, name)
            self.setToolTip(name)
        else:
            self.setFixedWidth(self.maximum_width)
            text = metrics.elidedText(name, Qt.ElideRight,
                                      self.width())
            self.setItemText(index, text)
            self.setToolTip(text)
        self.signal_change_theme.emit(self.current_theme)

    def add_item(self, text):
        self.addItem('❀ ' + text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and \
                self.rect().contains(event.pos()):
            self.clicked.emit()
            self.showPopup()

    def set_themes(self, themes):
        self.clear()
        if self.current_theme:
            self.themes = [self.current_theme]
            self.add_item(self.current_theme)
        else:
            self.themes = []
        for theme in themes:
            if theme not in self.themes:
                self.add_item(theme)
                self.themes.append(theme)
