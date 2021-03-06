from PyQt4.QtGui import QMainWindow, QShortcut, QKeySequence, QApplication, QIcon
from PyQt4.QtCore import Qt
from shiro.library import Library
from shiro.ui.widgets import kviewers
import os


class ReaderWindow(QMainWindow):
    def __init__(self, parent, chapter, view_mode=None):
        super(ReaderWindow, self).__init__()
        self._parent = parent
        self.chapter = chapter
        self.view_container = None
        self.load_chapter(chapter, view_mode)

        self.global_shortcuts = []

        self.setWindowIcon(QIcon('icon.ico'))
        self.setCentralWidget(self.view_container)
        self.setGeometry(0, 0, 1200, 800)
        self.center_window()
        self.define_global_shortcuts()

    def define_global_shortcuts(self):
        sequence = {
            'Ctrl+Shift+Left': self.view_container.prev_chapter,
            'Ctrl+Left': self.view_container.first_page,
            'Left': self.view_container.page_up,
            'Right': self.view_container.page_down,
            'Space': self.view_container.page_down,
            'Ctrl+Right': self.view_container.last_page,
            'Ctrl+Shift+Right': self.view_container.next_chapter,
            'Ctrl+R': self.view_container.rotate_right,
            'Ctrl+Shift+R': self.view_container.rotate_left,
            'Ctrl+B': self.view_container.first_page,
            'Ctrl+E': self.view_container.last_page,
            'S': self.switch_double_page_direction,
            'D': self.switch_double_page,
            'M': self.switch_viewing_modes,
            '1': self.view_container.original_fit,
            '2': self.view_container.vertical_fit,
            '3': self.view_container.horizontal_fit,
            '4': self.view_container.best_fit,
            'Q': self.close,
        }

        for key, value in sequence.items():
            s = QShortcut(QKeySequence(key), self.view_container, value)
            s.setEnabled(True)
            self.global_shortcuts.append(s)

    def center_window(self):
        frame_geometry = self.frameGeometry()
        monitor_screen_index = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(monitor_screen_index).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def load_chapter(self, chapter, view_mode=None):
        file_path = os.path.join(Library.directory, chapter.parent.title, chapter.get_file_name())
        if os.path.isfile(file_path) and view_mode is not 'web':
            self.load_chapter_offline(chapter, view_mode)
        else:
            self.load_chapter_online(chapter)

    def load_chapter_offline(self, chapter, view_mode=None):
        if type(self.view_container) == kviewers.KWebViewer or self.view_container is None:
            if view_mode is 'double':
                self.view_container = kviewers.KDoublePageViewer(self, chapter)
            else:
                self.view_container = kviewers.KPageViewer(self, chapter)
            self.setCentralWidget(self.view_container)
        else:
            self.view_container.load_chapter(chapter)

    def load_chapter_online(self, chapter):
        if type(self.view_container) != kviewers.KWebViewer:
            self.view_container = kviewers.KWebViewer(self, chapter)
            self.setCentralWidget(self.view_container)
        else:
            self.view_container.load_chapter(chapter)

    def full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:
            self.full_screen()

    def resizeEvent(self, event):
        self.view_container.reload()

    def switch_viewing_modes(self):
        if type(self.view_container) == kviewers.KPageViewer or type(self.view_container) == kviewers.KDoublePageViewer:
            self.load_chapter_online(self.chapter)
        else:
            file_name = os.path.join(Library.directory, self.chapter.parent.title, self.chapter.get_file_name())
            if not os.path.isfile(file_name):
                return
            self.load_chapter_offline(self.chapter)
        self.global_shortcuts = []
        self.define_global_shortcuts()

    def switch_double_page(self):
        typ = type(self.view_container)
        if typ == kviewers.KWebViewer:
            return

        current_page = self.view_container.current_page
        chapter = self.view_container.chapter
        if typ == kviewers.KPageViewer:
            self.view_container = kviewers.KDoublePageViewer(self, chapter, current_page)
            self.view_container.reload()
            self.view_container.scroll_to_top()
        else:
            self.view_container = kviewers.KPageViewer(self, chapter, current_page)
        self.setCentralWidget(self.view_container)
        self.global_shortcuts = []
        self.define_global_shortcuts()

    def switch_double_page_direction(self):
        if type(self.view_container) == kviewers.KDoublePageViewer:
            self.view_container.switch_directions()

    def closeEvent(self, *args, **kwargs):
        self._parent.update_chapter_table()


