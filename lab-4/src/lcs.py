"""Longest Common Subsequence (LCS) using dynamic programming."""

from __future__ import annotations

import argparse


def _length_table(first: str, second: str) -> list[list[int]]:
    """Build table[i][j] containing the LCS length for two prefixes."""
    table = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    for i, left_character in enumerate(first, start=1):
        for j, right_character in enumerate(second, start=1):
            if left_character == right_character:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table


def longest_common_subsequence(first: str, second: str) -> str:
    """Return one longest subsequence shared by *first* and *second*."""
    table = _length_table(first, second)
    i, j = len(first), len(second)
    reversed_result: list[str] = []

    # Walk backwards from the bottom-right cell to reconstruct an actual LCS.
    while i > 0 and j > 0:
        if first[i - 1] == second[j - 1]:
            reversed_result.append(first[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] > table[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(reversed_result))


def lcs_length(first: str, second: str) -> int:
    """Return the length of an LCS."""
    return _length_table(first, second)[-1][-1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Find a longest common subsequence.")
    parser.add_argument("first", nargs="?", default="ABCBDAB")
    parser.add_argument("second", nargs="?", default="BDCABA")
    args = parser.parse_args()
    result = longest_common_subsequence(args.first, args.second)
    print(f"First string: {args.first}")
    print(f"Second string: {args.second}")
    print(f"LCS: {result}")
    print(f"Length: {len(result)}")


if __name__ == "__main__":
    main()
