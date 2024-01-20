import re


def remove_text_between_angle_brackets(input_string: str) -> str:
    # Define a regular expression pattern to match text between < and >
    pattern = re.compile(r"<.*?>")
    # Use sub() function to replace the matched pattern with an empty string
    result_string = re.sub(pattern, "", input_string)
    return result_string


def clean_text(x: str) -> str:
    return x.replace("\n", " ")
