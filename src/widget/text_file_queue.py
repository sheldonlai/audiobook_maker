import os
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHeaderView, QSizePolicy, QTableWidget,
                               QTableWidgetItem, QVBoxLayout, QWidget)


class TextFileQueue(QWidget):
    def __init__(self):
        super().__init__()
        self.active_path = None
        self.queue = []
        self.queue_widget = QTableWidget()
        self.queue_widget.setColumnCount(1)  # One column for file paths
        self.queue_widget.setHorizontalHeaderLabels(["File Paths"])
        self.queue_widget.setRowCount(0)

        self.queue_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.queue_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow table to expand
        self.queue_widget.setWordWrap(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.queue_widget)

    def reset_widget(self):
        self.queue_widget.setRowCount(0)
        self.queue = []

    def updateView(self, active_file_path: str, file_queue: List[str]):
        self.reset_widget()
        self.queue = file_queue
        self.active_path = active_file_path

        if active_file_path not in file_queue:
            raise Exception(
                "activeFilePath={} not found in the given file queue={}", active_file_path, file_queue)

        total_sentences = len(file_queue)
        # Set the total number of rows upfront
        self.queue_widget.setRowCount(total_sentences)

        relative_display_paths = self.__extract_relative_paths_for_display(
            file_queue)
        for index, file_path in enumerate(relative_display_paths):
            self.__add_text_file_queue_item(file_path, index)

        for index, file_path in enumerate(file_queue):
            if (file_path == active_file_path):
                self.__set_text_file_row_active(index)

    def get_audiobook_subdirectory(self):

        common_prefix = self.__extract_common_prefix(self.queue)
        print("get_audiobook_subdirectory common_prefix={}, active_path={}\n".format(
            common_prefix, self.active_path))
        return self.__strip_extension(os.path.relpath(self.active_path, common_prefix))

    def get_next_file_path(self):
        index = self.queue.index(self.active_path)
        if index < len(self.queue) - 1:
            return self.queue[index + 1]
        else:
            return None  # x is the last element

    def __add_text_file_queue_item(self, filePath, index):
        self.queue_widget.blockSignals(True)
        item = QTableWidgetItem(filePath)
        item.setText(filePath)
        self.queue_widget.setItem(index, 0, item)

        self.queue_widget.blockSignals(False)

    def __set_text_file_row_active(self, row):
        self.queue_widget.blockSignals(True)
        queueItem = self.queue_widget.item(row, 0)
        if queueItem:
            queueItem.setBackground(Qt.green)
        self.queue_widget.blockSignals(False)

    def __extract_relative_paths_for_display(self, path_list):
        common_prefix = os.path.commonprefix(path_list)
        return [os.path.relpath(path, common_prefix) for path in path_list]

    def __extract_common_prefix(self, path_list):
        folder_path_list = [os.path.split(e)[0] for e in path_list]
        if len(path_list) == 1:
            return folder_path_list[0]
        return os.path.commonprefix(folder_path_list)

    def __strip_extension(self, filename):
        return os.path.splitext(filename)[0]
