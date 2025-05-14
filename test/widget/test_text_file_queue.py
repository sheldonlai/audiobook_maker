import os
import unittest
from unittest.mock import patch, MagicMock

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

# Assuming your class is in text_file_queue.py
from src.widget.text_file_queue import TextFileQueue


class TestTextFileQueue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])  # Initialize Qt app for testing

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def setUp(self):
        self.text_file_queue = TextFileQueue()

    def tearDown(self):
        self.text_file_queue.reset_widget()  # Important: Reset after each test

    def test_updateView_valid_input(self):
        file_queue = ["/path/to/file1.txt",
                      "/path/to/file2.txt", "/path/to/file3.txt"]
        active_file_path = "/path/to/file2.txt"
        self.text_file_queue.updateView(active_file_path, file_queue)

        self.assertEqual(self.text_file_queue.queue, file_queue)
        self.assertEqual(
            self.text_file_queue.queue_widget.rowCount(), len(file_queue))
        self.assertEqual(self.text_file_queue.active_path, active_file_path)

        # Check if the active row is highlighted (using a simplified check)
        active_item = self.text_file_queue.queue_widget.item(
            1, 0)  # Index 1 for file2.txt
        # check background color
        self.assertEqual(active_item.background(), Qt.green)

    def test_updateView_active_path_not_in_queue(self):
        file_queue = ["/path/to/file1.txt", "/path/to/file2.txt"]
        active_file_path = "/path/to/file3.txt"  # Not in the queue

        with self.assertRaisesRegex(Exception, "activeFilePath=.+ not found in the given file queue=.+"):
            self.text_file_queue.updateView(active_file_path, file_queue)

    def test_get_audiobook_subdirectory(self):
        file_queue = ["/path/to/audiobook/file1.txt",
                      "/path/to/audiobook/file2.txt", "/path/to/audiobook/file3.txt"]
        active_file_path = "/path/to/audiobook/file2.txt"
        self.text_file_queue.updateView(active_file_path, file_queue)

        subdir = self.text_file_queue.get_audiobook_subdirectory()
        # Expecting the filename without extension
        self.assertEqual(subdir, "file2")

    def test_get_audiobook_subdirectory_single_file(self):
        file_queue = ["/path/to/audiobook/file1.txt"]
        active_file_path = "/path/to/audiobook/file1.txt"
        self.text_file_queue.updateView(active_file_path, file_queue)

        subdir = self.text_file_queue.get_audiobook_subdirectory()
        self.assertEqual(subdir, "file1")

    def test_get_next_file_path(self):
        file_queue = ["/path/to/file1.txt",
                      "/path/to/file2.txt", "/path/to/file3.txt"]
        active_file_path = "/path/to/file2.txt"
        self.text_file_queue.updateView(active_file_path, file_queue)

        next_file = self.text_file_queue.get_next_file_path()
        self.assertEqual(next_file, "/path/to/file3.txt")

    def test_get_next_file_path_last_file(self):
        file_queue = ["/path/to/file1.txt",
                      "/path/to/file2.txt", "/path/to/file3.txt"]
        active_file_path = "/path/to/file3.txt"  # Last file
        self.text_file_queue.updateView(active_file_path, file_queue)

        next_file = self.text_file_queue.get_next_file_path()
        self.assertIsNone(next_file)

    def test_extract_relative_paths_for_display_multi_depths_files(self):
        paths = ["/path/to/audiobook/ch101/file1.txt",
                 "/path/to/audiobook/ch101/file2.txt", "/path/to/audiobook/ch102/file3.txt"]
        expected_relative_paths = ["ch101\\file1.txt",
                                   "ch101\\file2.txt", "ch102\\file3.txt"]
        relative_paths = self.text_file_queue._TextFileQueue__extract_relative_paths_for_display(
            paths)
        self.assertEqual(relative_paths, expected_relative_paths)

    def test_extract_relative_paths_for_display(self):
        paths = ["/path/to/audiobook/file1.txt",
                 "/path/to/audiobook/file2.txt", "/path/to/audiobook/file3.txt"]
        expected_relative_paths = ["file1.txt", "file2.txt", "file3.txt"]
        relative_paths = self.text_file_queue._TextFileQueue__extract_relative_paths_for_display(
            paths)
        self.assertEqual(relative_paths, expected_relative_paths)

    def test_extract_relative_paths_for_displaying_single_path(self):
        paths = ["/path/to/audiobook/file1.txt"]
        expected_relative_paths = ["file1.txt"]
        relative_paths = self.text_file_queue._TextFileQueue__extract_relative_paths_for_display(
            paths)
        self.assertEqual(relative_paths, expected_relative_paths)

    def test_extract_common_prefix(self):
        paths = ["/path/to/audiobook/file1.txt",
                 "/path/to/audiobook/file2.txt", "/path/to/audiobook/file3.txt"]
        expected_prefix = "/path/to/audiobook"
        prefix = self.text_file_queue._TextFileQueue__extract_common_prefix(
            paths)
        self.assertEqual(prefix, os.path.normpath(expected_prefix))

    def test_extract_common_prefix_single_file(self):
        paths = ["/path/to/audiobook/file1.txt"]
        expected_prefix = "/path/to/audiobook"
        prefix = self.text_file_queue._TextFileQueue__extract_common_prefix(
            paths)
        self.assertEqual(prefix, expected_prefix)

    def test_extract_common_prefix_single_file(self):
        paths = []
        expected_prefix = ""
        prefix = self.text_file_queue._TextFileQueue__extract_common_prefix(
            paths)
        self.assertEqual(prefix, expected_prefix)

    def test_strip_extension(self):
        filename = "myfile.txt"
        expected_filename = "myfile"
        stripped_filename = self.text_file_queue._TextFileQueue__strip_extension(
            filename)
        self.assertEqual(stripped_filename, expected_filename)


if __name__ == '__main__':
    unittest.main()
