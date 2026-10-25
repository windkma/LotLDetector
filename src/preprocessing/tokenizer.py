"""
Command line tokenizer for Windows CMD and Linux POSIX shells.
"""

import re
import shlex

_RE_WIN_CMD = re.compile(
    r'"((?:""|\\[\"\\]|[^"])*)?"?()|(\\\\(?=\\*")|\\")|(&&?|\|\|?|\d?>|[<])'
    r'|([^\s"&|<>]+)|(\s+)|(.)'
)


def _split_once_windows(s: str) -> list:
    args = []
    accu = None
    for qs, qss, esc, pipe, word, white, fail in _RE_WIN_CMD.findall(s):
        if word:
            pass
        elif esc:
            word = esc[1]
        elif white or pipe:
            if accu is not None:
                args.append(accu)
            if pipe:
                args.append(pipe)
            accu = None
            continue
        elif fail:
            continue
        elif qs:
            word = qs.replace('\\"', '"').replace('\\\\', '\\').replace('""', '"')
        else:
            word = qss

        accu = (accu or '') + word

    if accu is not None:
        args.append(accu)

    return args


def split_windows(command: str) -> list:
    """
    Tokenize Windows command lines with iterative quote resolution.
    """
    s = command.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]

    current = [s]
    while True:
        expanded = []
        for tok in current:
            if tok.startswith('"') and tok.endswith('"'):
                tok = tok[1:-1]
            parts = _split_once_windows(tok)
            expanded.extend(parts)
        if expanded == current:
            break
        current = expanded

    return current


def split_linux(command: str) -> list:
    """
    Tokenize Linux POSIX command lines using iterative shlex parsing.
    """
    def _split_once(s: str) -> list:
        try:
            lex = shlex.shlex(s, punctuation_chars=True, posix=True)
            lex.whitespace_split = False
            return list(lex)
        except ValueError:
            return [s]

    current = [command]
    while True:
        expanded = []
        for tok in current:
            parts = _split_once(tok)
            expanded.extend(parts)
        if expanded == current:
            break
        current = expanded

    return current
