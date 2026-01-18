import sys
import itertools


def read_pieces_from_file(filename):
    pieces = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        raw_items = content.replace(',', '\n').splitlines()
        for item in raw_items:
            cleaned = item.strip()
            if cleaned:
                pieces.append(cleaned)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        sys.exit(1)
    return pieces


def read_pieces_interactive():
    print("\nEnter pieces of information (one per line)")
    print("Press Enter twice (empty line) to finish\n")

    pieces = []
    while True:
        line = input().strip()
        if not line and pieces:
            break
        if line:
            pieces.append(line)
    return pieces


def ask_max_words(default=14000):
    while True:
        print(f"\nMaximum number of words? (default: {default:,})")
        answer = input("> ").strip()
        if not answer:
            return default
        try:
            value = int(answer)
            if value < 1000:
                print("Please use at least 1000 or press Enter.")
                continue
            return value
        except ValueError:
            print("Enter a number or press Enter for default.")


def generate_wordlist(pieces, max_words=14000):
    words = set()

    # ── 1. Singles + all useful case variations ─────────────────────────────
    for p in pieces:
        words.add(p)
        words.add(p.lower())
        words.add(p.capitalize())
        words.add(p.upper())
        words.add(p.title())  # EachWordLikeThis

    # ── 2. Massive realistic suffixes (2024–2026 breach patterns) ───────────
    suffixes = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        '01', '00', '10', '11', '12', '21', '22', '69', '88', '99',
        '123', '1234', '12345', '123456', '123!', '1234!',
        '!', '@', '#', '$', '*', '!!', '!@', '@@', '#1', '!*',
        '2023', '2024', '2025', '2026', '2020', '2019', '2018',
        '2000', '1990', '1999', '1980', 'pass', 'admin', 'qwerty'
    ]

    # Apply suffixes to all current words (singles + cases)
    current_words = list(words)  # copy to avoid modifying while iterating
    for w in current_words:
        for s in suffixes:
            candidate = w + s
            if 6 <= len(candidate) <= 20:  # realistic password length filter
                words.add(candidate)
            if len(words) >= max_words:
                return sorted(words)[:max_words]

    # ── 3. Intentional doubles (very common) ────────────────────────────────
    for p in pieces:
        double = p + p
        words.add(double)
        words.add(double.lower())
        double_cap = p.capitalize() + p.capitalize()
        words.add(double_cap)
        if len(words) >= max_words:
            return sorted(words)[:max_words]

    # ── 4. Pairs (only 2 pieces) with separators ────────────────────────────
    for combo in itertools.product(pieces, repeat=2):
        # No separator
        joined = ''.join(combo)
        if 6 <= len(joined) <= 20:
            words.add(joined)
            words.add(joined.lower())

        # Common separators
        for sep in ['.', '-', '_', ' ']:
            joined_sep = sep.join(combo)
            if 6 <= len(joined_sep) <= 20:
                words.add(joined_sep)
                words.add(joined_sep.lower())

        if len(words) >= max_words:
            return sorted(words)[:max_words]

    # ── 5. Few useful prefixes — mostly on singles (prefixes are rare) ───────
    prefixes = ['!', '@', '#', '$', '!!', '1', '12', '123', 'the', 'my']
    current_words = list(words)
    for w in current_words:
        for pre in prefixes:
            candidate = pre + w
            if 6 <= len(candidate) <= 20:
                words.add(candidate)
            if len(words) >= max_words:
                return sorted(words)[:max_words]

    return sorted(words)[:max_words]


def main():
    print("Custom wordlist generator — pairs + massive suffixes/prefixes\n")

    pieces = []
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print(f"Reading from file: {filename}")
        pieces = read_pieces_from_file(filename)
    else:
        pieces = read_pieces_interactive()

    pieces = list(set(pieces))  # remove duplicates

    if not pieces:
        print("No pieces provided. Exiting.")
        return

    max_words = ask_max_words()

    print(f"\nWorking with {len(pieces)} unique pieces")
    print(f"Generating up to {max_words:,} realistic passwords...")

    wordlist = generate_wordlist(pieces, max_words=max_words)

    output_file = "wordlist.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for w in wordlist:
            f.write(w + '\n')

    print(f"\nFinished!")
    print(f"Generated {len(wordlist):,} unique entries")
    print(f"Saved to: {output_file}")
    if len(wordlist) >= max_words:
        print("→ Reached your requested limit")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user")
        sys.exit(0)