"""
Command line normalizer and deobfuscation utilities.
"""

import re
from ipaddress import ip_address

_RE_IPV4 = re.compile(
    r"[^\w^\d]((?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)[^\w^\d]"
)
_RE_CARET = re.compile(r"\^")


def deobfuscate_cmd(command: str) -> str:
    """
    Remove Windows CMD caret obfuscation characters.
    Example: 'c^e^r^t^u^t^i^l.exe' -> 'certutil.exe'
    """
    return _RE_CARET.sub("", command)


def extract_ip_labels(command: str) -> list:
    """
    Extract IPv4 addresses and classify into semantic network labels:
    IP_LOOPBACK, IP_PRIVATE, IP_LINK_LOCAL, IP_MULTICAST, IP_RESERVED,
    IP_PUBLIC, IP_UNSPECIFIED.
    """
    labels = {}
    try:
        matches = _RE_IPV4.finditer(f" {command} ")
        for match in matches:
            try:
                clean_ip = "".join(ch for ch in match.group(0) if ch.isalnum() or ch == ".")
                ipt = ip_address(clean_ip)
                if ipt.is_link_local:
                    resp = "link_local"
                elif ipt.is_loopback:
                    resp = "loopback"
                elif ipt.is_multicast:
                    resp = "multicast"
                elif ipt.is_private:
                    resp = "private"
                elif ipt.is_reserved:
                    resp = "reserved"
                elif ipt.is_unspecified:
                    resp = "unspecified"
                elif ipt.is_global:
                    resp = "public"
                else:
                    resp = "public"

                label = f"IP_{resp.upper()}"
                labels[label] = 0
            except ValueError:
                continue
    except Exception:
        pass

    return list(labels.keys())
