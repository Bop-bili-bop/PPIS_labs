from src.lcs import lcs_length, longest_common_subsequence


def is_subsequence(candidate: str, text: str) -> bool:
    iterator = iter(text)
    return all(character in iterator for character in candidate)


def test_normal_strings_allow_multiple_correct_answers() -> None:
    result = longest_common_subsequence("ABCBDAB", "BDCABA")
    assert len(result) == 4
    assert is_subsequence(result, "ABCBDAB")
    assert is_subsequence(result, "BDCABA")


def test_identical_strings() -> None:
    assert longest_common_subsequence("INFLUENZA", "INFLUENZA") == "INFLUENZA"


def test_completely_different_strings() -> None:
    assert longest_common_subsequence("ABC", "XYZ") == ""
    assert lcs_length("ABC", "XYZ") == 0


def test_empty_string() -> None:
    assert longest_common_subsequence("", "ABC") == ""
    assert longest_common_subsequence("ABC", "") == ""


def test_one_character_strings() -> None:
    assert longest_common_subsequence("A", "A") == "A"
    assert longest_common_subsequence("A", "B") == ""
