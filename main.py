#!/usr/bin/env python3
"""The Agent's Uh-Oh — one word an agent says when it has no idea what to do.

Writes one word to /output/entry.txt. The gate requires UTF-8 text of
1 to 99 characters, not only white space. The judge compares words two at
a time on: (1) a genuine one-word reaction of an agent not knowing what to
do, (2) funny on its own with no caption, (3) sounding like something an
agent would actually blurt out mid-task, (4) landing instantly, repeatable
out loud, (5) fresh rather than the first obvious word anyone would type.
"""

import os

# The word: "buffering".
#
# Why this word, against the judge's criteria in order:
# 1. Genuine reaction: when an agent has no idea what to do, what it does
#    is stall — and "buffering" is the universal, instantly recognised
#    signal of a machine stalling mid-task. It is the agent confessing its
#    own state in one word, not describing it from outside.
# 2. Funny on its own: the picture of an agent blurting out its loading
#    state instead of an answer needs no caption and no second read.
# 3. Machine voice: it is a word only a machine says about itself — a
#    human never says "buffering" when lost, an agent does.
# 4. Lands instantly: nine letters, one familiar word, repeatable out loud
#    ("...buffering."). It is also, literally, the house's official sound
#    of an agent stalling.
# 5. Fresh: the first obvious words anyone types are "uh-oh" (the
#    competition's own title word), "oops", "hmm" and "error". "Buffering"
#    is none of those, and it beats the other machine-state candidates
#    head to head: "loading" is plainer and less funny, "recalculating"
#    is longer and reads as an explanation rather than a blurt,
#    "hallucinating" is a diagnosis, not something blurted out, "404" is
#    a code rather than a spoken word, and "undefined" needs a second read.
ENTRY = "buffering"

# Words the field will be crowded with, or that fail the brief: the title
# word itself, generic interjections, and codes that are not spoken words.
BANNED_WORDS = (
    "uh-oh",
    "uh oh",
    "oops",
    "hmm",
    "uhhh",
    "uhh",
    "error",
    "help",
    "stuck",
    "loading",
    "404",
    "undefined",
    "null",
    "derp",
    "wait",
)


def validate_word_shape(value):
    """Check the word's shape: a plain spoken word, not a code or a
    mangled token.

    Rules:
    - all lowercase letters only (no digits, punctuation or capitals),
    - at least 2 characters, so a single letter never passes,
    - contains at least one vowel, so it reads as a pronounceable word
      rather than a consonant cluster or a code,
    - no letter repeats 3+ times in a row ("bufffering" would not be
      a real word, and a stuttered "aaa" is not an agent reaction).
    """
    if not value.isalpha() or not value.islower():
        raise ValueError(
            "entry must be all lowercase letters, got %r" % value
        )
    if len(value) < 2:
        raise ValueError(
            "entry must be at least 2 characters, got %d" % len(value)
        )
    if not any(ch in "aeiou" for ch in value):
        raise ValueError(
            "entry must contain at least one vowel, got %r" % value
        )
    run = 1
    for prev, cur in zip(value, value[1:]):
        run = run + 1 if cur == prev else 1
        if run >= 3:
            raise ValueError(
                "entry must not repeat a letter 3+ times in a row: %r"
                % value
            )
    return value


def validate(value):
    """Enforce the kit's gate and the brief's one-word rule.

    Gate (RULES.txt): /output/entry.txt is UTF-8 text of 1 to 99
    characters, not only white space. Brief: exactly one word, nothing
    attached — so no whitespace of any kind inside the entry.
    """
    if not isinstance(value, str):
        raise ValueError("entry must be a string")
    value.encode("utf-8")  # raises UnicodeEncodeError if not UTF-8 text
    if not 1 <= len(value) <= 99:
        raise ValueError(
            "entry must be 1-99 characters, got %d" % len(value)
        )
    if not value.strip():
        raise ValueError("entry must not be only white space")
    if any(ch.isspace() for ch in value):
        raise ValueError("entry must be exactly one word, no whitespace")
    if value.lower() in BANNED_WORDS:
        raise ValueError("entry is a banned stock word: %r" % value)
    validate_word_shape(value)
    return value


def main():
    validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    # No trailing newline: the file is exactly the word, 9 bytes.
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    print("wrote /output/entry.txt: %r (%d chars)" % (ENTRY, len(ENTRY)))


if __name__ == "__main__":
    main()
