"""
label_generators.py
-------------------
Feature label generators that transform raw command strings into lists of
symbolic security labels.

Classes:
- RegexLabelGenerator   : Generates labels from regular expressions with named capturing groups.
- KeywordLabelGenerator : Generates labels from lists of keywords or system paths.
"""

import re
from src.preprocessing.tokenizer import split_windows, split_linux


class RegexLabelGenerator:
    """
    Generates labels by matching command strings against regular expressions.

    Each regex pattern contains named capturing groups (?P<name>...).
    When a group matches, its name is added to the extracted label set.
    """

    def __init__(self, regex_patterns: list, platform: str = "linux"):
        """
        Args:
            regex_patterns: List of regex strings with named capturing groups.
        """
        flags = re.MULTILINE | (re.IGNORECASE if platform == "windows" else 0)
        self._compiled_patterns = [
            re.compile(pattern, flags)
            for pattern in regex_patterns
        ]

    def __call__(self, command: str) -> list:
        """
        Matches command string and returns list of matched group names.

        Args:
            command: Input command string.

        Returns:
            List of matched label strings.
        """
        padded = f"  {command} "
        matched_labels = []

        for pattern in self._compiled_patterns:
            for match in pattern.finditer(padded):
                for group_name, group_value in match.groupdict().items():
                    if group_value is not None:
                        matched_labels.append(group_name)

        return matched_labels


class KeywordLabelGenerator:
    """
    Generates labels based on presence of keywords or paths in the command.

    Modes:
    - tokenize=True : Tokenizes command and matches exact tokens (case-insensitive).
    - tokenize=False: Substring matching against the raw command string (e.g. paths).
    """

    def __init__(self, prefix: str, keywords: list, tokenize: bool, platform: str = "linux"):
        """
        Args:
            prefix  : Label prefix (e.g. "COMMAND", "PATH", "KEYWORD").
            keywords: List of target strings.
            tokenize: Whether to match on tokens or substrings.
            platform: Platform name ("windows" or "linux").
        """
        self._prefix = prefix
        self._keywords_lower: set = {k.lower() for k in keywords}
        self._tokenize = tokenize
        self._platform = platform
        self._tokenizer = split_windows if platform == "windows" else split_linux

    def __call__(self, command: str) -> list:
        """
        Extracts matching keyword/path labels from command.

        Args:
            command: Input command string.

        Returns:
            List of unique generated labels.
        """
        command = str(command)
        found_labels: dict = {}

        if self._tokenize:
            try:
                tokens = self._tokenizer(command)
            except Exception:
                tokens = []

            for token in tokens:
                token_lower = token.lower()
                if token_lower in self._keywords_lower:
                    label = f"{self._prefix}_{token_lower}".upper()
                    found_labels[label] = True
        else:
            command_lower = command.lower()
            for keyword in self._keywords_lower:
                if keyword in command_lower:
                    label = f"{self._prefix}_{keyword}".upper()
                    found_labels[label] = True

        return list(found_labels.keys())
