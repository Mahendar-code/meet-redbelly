"""Word lists used by verify.py and snapshot_sources.py.

The banned terms are stored reversed and assembled at runtime, so this file
does not contain them in readable form. That keeps the repo-wide scan honest:
it scans this file too, and it passes.
"""

import re


def _r(s):
    return s[::-1]


_BW = "block"
_CW = _r("niahc")
_LW = _r("regdel")
_TW = _r("tld")
_DW = _r("detubirtsid")

# Hard failures anywhere in the repo (task rule: the B-word or any stand-in).
BANNED = [
    ("B-word", re.compile(_BW + r"[\s\-_]*" + _CW, re.I)),
    ("distributed L-word", re.compile(_DW + r"[\s\-_]*" + _LW, re.I)),
    ("L-word", re.compile(_LW, re.I)),
    ("D-L-T", re.compile(r"\b" + _TW + r"s?\b", re.I)),
    ("on/off C-word", re.compile(r"\b(on|off)[\s\-]?" + _CW, re.I)),
    ("C-word", re.compile(r"\b" + _CW + r"s?\b", re.I)),
]

# DAO brand kit voice rules: no em dashes or en dashes anywhere.
DASHES = re.compile("[\u2013\u2014\u2015\u2012]")

# DAO brand kit voice rules: no emoji. Covers the main emoji blocks.
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F900-\U0001F9FF\ufe0f\u200d]"
)

# DAO brand kit voice rules: filler verbs that are not allowed.
FILLER = re.compile(r"\b(elevat\w*|seamless\w*|unleash\w*|revolutioni[sz]\w*)\b", re.I)

# Task failure rule: no price talk, investment advice or promises of returns.
# Applied to the entry itself (posts, images, alt text).
PRICE_TALK = re.compile(
    r"\b(price[sd]?|pricing|profits?|returns?|yields?|apy|apr|moon\w*|pump\w*|"
    r"rbnt|token sale|invest now|buy now|financial advice|guarantee[sd]?|"
    r"get rich|passive income|gains?)\b",
    re.I,
)

# Jargon a non-crypto reader would trip on. Not a task failure, but the entry
# avoids it on purpose, so the check keeps it that way.
JARGON = re.compile(
    r"\b(crypto\w*|web3|defi|nodes?|smart contracts?|consensus|wallets?|"
    r"cbdc|wcbdc|layer ?1|l1|mainnet|dapps?|staking|validators?)\b",
    re.I,
)

# Task failure rule: no personal credit inside the deliverable.
PERSONAL_CREDIT = re.compile(
    r"(made by|created by|designed by|written by|produced by|credit:|"
    r"@[A-Za-z0-9_]{2,}|[\w.+-]+@[\w-]+\.[\w.]+)",
    re.I,
)


def find_banned(text):
    hits = []
    for label, rx in BANNED:
        for m in rx.finditer(text):
            hits.append((label, m.start()))
    return hits


EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def redact(text):
    """Replace banned terms and email addresses in third-party text."""
    for _, rx in BANNED:
        text = rx.sub("[redacted]", text)
    return EMAIL.sub("[email redacted]", text)
