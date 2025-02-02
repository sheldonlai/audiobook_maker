import re
import inflect

engine = inflect.engine()


def format_chapter_title(sentence):
    """
    Formats chapter titles, converting numbers to English and part numbers.

    Args:
        title: The chapter title string.

    Returns:
        The formatted chapter title, or None if the title doesn't start with "chapter".
    """

    sentence = sentence.strip()  # Remove leading/trailing whitespace

    if not sentence.lower().startswith("chapter"):
        return sentence

    # Regex to capture chapter number and part number
    match = re.match(r"^Chapter\s+(\d+)(.+?)\s*\((\d+)\)$",
                     sentence, re.IGNORECASE)
    if match:
        chapter_num = int(match.group(1))
        chapter_title = match.group(2)
        part_num = int(match.group(3))

        formatted_chapter_num = engine.number_to_words(chapter_num)
        formatted_chapter_num = formatted_chapter_num.replace(
            ",", "")  # remove commas for better reading

        formatted_part_num = engine.number_to_words(part_num)
        chapter_title = _add_period_if_missing(chapter_title) 

        return f"Chapter {formatted_chapter_num}{chapter_title} Part {formatted_part_num}."

    # Handle cases without part numbers
    match = re.match(r"^Chapter\s+(\d+)(.+)$", sentence, re.IGNORECASE)
    if match:
        chapter_num = int(match.group(1))
        chapter_title = match.group(2)

        formatted_chapter_num = engine.number_to_words(
            chapter_num)
        formatted_chapter_num = formatted_chapter_num.replace(",", "")
        chapter_title = _add_period_if_missing(chapter_title) 

        return f"Chapter {formatted_chapter_num}{chapter_title}"

    return sentence

def _add_period_if_missing(text):  # Helper function (can be outside the main function)
    """Adds a period if the text doesn't end with punctuation."""
    if not re.search(r'[.?!;:]$', text):
        return text + "."
    return text