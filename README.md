# whatsappy


Some simple functions to parse whatsapp log files
into pandas dataframes.

## Installation

For the moment, just clone this repo and pip install it locally

```bash
git clone https://github.com/jeiros/whatsappy.git
cd whatsappy
pip install -r requirements.txt
pip install .
```

## Example
Email yourself a copy of a conversation log file. Save it as a `.txt` file.

Load it into a pandas DataFrame like this:

```python
from whatsappy import get_all_lines, parse_lines_into_df
lines = get_all_lines('path/to/your/file.txt')
df = parse_lines_into_df(lines, log_type='android')
```