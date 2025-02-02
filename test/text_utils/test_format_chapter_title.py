import unittest
from src.text_utils.format_chapter_title import format_chapter_title


class TestFormatChapterTitle(unittest.TestCase):

    def test_valid_chapter_title(self):
        title = "Chapter 160: Isn't It Better to Strike First? (2)"
        expected = "Chapter one hundred and sixty: Isn't It Better to Strike First? Part two."
        self.assertEqual(format_chapter_title(title), expected)

    def test_invalid_chapter_title(self):
        title = "Section 1: Introduction"
        self.assertEqual(format_chapter_title(title), title)

    def test_chapter_title_no_part(self):
        title = "Chapter 560: Introduction to integrals"
        expected = "Chapter five hundred and sixty: Introduction to integrals."
        self.assertEqual(format_chapter_title(title), expected)

    def test_chapter_with_single_digit_part(self):
        title = "Chapter 20: We Need a Variable (5)"
        expected = "Chapter twenty: We Need a Variable. Part five."
        self.assertEqual(format_chapter_title(title), expected)

    def test_chapter_title_empty(self):
        title = ""
        self.assertEqual(format_chapter_title(title), title)

    def test_chapter_title_long_title(self):
        title = "Chapter 1: This is a very long title that should not cause any problems (1)"
        # Adjust the expected string
        expected = "Chapter one: This is a very long title that should not cause any problems. Part one."
        self.assertEqual(format_chapter_title(title), expected)

    def test_chapter_title_numbers_in_title(self):
        title = "Chapter 1: 10 Things to Consider (1)"
        expected = "Chapter one: 10 Things to Consider. Part one."
        self.assertEqual(format_chapter_title(title), expected)

    def test_chapter_title_parentheses_in_title(self):
        title = "Chapter 1: (Important) Stuff to Remember (1)"
        expected = "Chapter one: (Important) Stuff to Remember. Part one."
        self.assertEqual(format_chapter_title(title), expected)

    def test_chapter_title_non_numeric_part(self):
        title = "Chapter 160: Isn't It Better to Strike First? (two)"
        expected = "Chapter one hundred and sixty: Isn't It Better to Strike First? (two)."
        self.assertEqual(format_chapter_title(title), expected)

    def test_chapter_title_mixed_case_spacing(self):
        title = "ChApTeR 160: IsN't It BeTtEr To StRiKe FiRsT?   (2)"
        expected = "Chapter one hundred and sixty: IsN't It BeTtEr To StRiKe FiRsT? Part two."
        self.assertEqual(format_chapter_title(title), expected)
    
    def test_title_without_colon(self):   
        title = "Chapter 22 You Madman, Why Would You Do That! (2)"
        expected = "Chapter twenty-two You Madman, Why Would You Do That! Part two."
        self.assertEqual(format_chapter_title(title), expected)


if __name__ == '__main__':
    unittest.main()
