- Interactive input (one piece per line) or file (txt/csv, commas or newlines)
- Removes duplicates automatically
- Generates:
  - All useful case variations
  - Huge list of realistic suffixes (years, numbers, symbols, common endings)
  - Intentional doubles (annaanna style)
  - Pairs of pieces (with and without common separators: . - _ space)
  - Small set of useful prefixes (mostly ! @ # $ etc.)
- Strict length filter (6–20 characters)
- Early stopping when reaching your desired limit
- Output saved as `wordlist.txt`

### Usage ###

Copy and paste main.py(preferably as wordlist.py)

```bash
# Interactive mode
python wordlist.py

# From file (txt or csv)
python wordlist.py info.txt
python wordlist.py person.csv
```
