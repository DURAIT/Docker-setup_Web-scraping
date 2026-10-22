# BBC News Headlines

A small Python script that fetches the BBC News front page and prints the top 5 headlines to the terminal.

## Example output

```
1. Australian MP loses both legs after alleged car attack, husband says
2. US citizen Stephen Hubbard freed by Russia as Trump envoy meets Putin
3. Katya Adler: France divided over who to blame for riots and what to learn from them
4. Pakistan arrests man wanted by US over $126m postage fraud case
5. Trump and Zelensky appear at loggerheads despite new optimism
```

## Requirements

- Python 3.9 or newer
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Setup

```
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
pip install requests beautifulsoup4
```

## Usage

```
python headlines.py
```

To check which tags the page is using (useful if the script stops finding headlines):

```
python headlines.py --inspect
```

This prints the number of `h1`/`h2`/`h3` tags, the most common `data-testid` values, and a few sample matches for the headline selector.

## How it works

1. **Fetch**: `requests` downloads `https://www.bbc.com/news` with a normal browser User-Agent, since some sites refuse the default Python one. The script checks that the status code is 200 before parsing anything, and exits with a clear message otherwise.
2. **Find headlines**: BeautifulSoup selects elements matching `[data-testid="card-headline"]`, the attribute BBC puts on the heading of each story card. If none are found, it falls back to any `<h2>` or `<h3>` tag.
3. **Clean**: whitespace is stripped and collapsed, and empty or duplicate headlines are skipped.
4. **Print**: up to 5 headlines are printed, numbered 1 to 5, one per line.

## Edge cases

- **Fewer than 5 headlines found**: prints what it found, plus a note such as `(Only 3 headline(s) found.)`.
- **No headlines found**: exits with a message suggesting `--inspect`.
- **Network error or non-200 response**: exits with an error message instead of a traceback.

## If BBC changes its layout

News sites change their markup from time to time. If the script stops returning proper headlines, run `--inspect`, find the tag or attribute that now holds the headlines, and update `PRIMARY_SELECTOR` at the top of `headlines.py`.

## Files

- `headlines.py`: the script
- `README.md`: this file
