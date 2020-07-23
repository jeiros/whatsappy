# whatsappy


Some simple functions to parse whatsapp log files
into pandas dataframes.

## Installation

Clone this repo and pip install it locally

```bash
git clone https://github.com/jeiros/whatsappy.git
cd whatsappy
pip install -r requirements.txt
pip install .
```

alternatively, use the [Docker image](https://hub.docker.com/r/jeiros/whatsappy)

```bash
docker run -it --rm -p 8888:8888 jeiros/whatsappy /bin/bash -c "jupyter notebook --ip="*" --port=8888 --no-browser --allow-root"
```



## Example
Email yourself a copy of a conversation log file. Save it as a `.txt` file.

Load it into a pandas DataFrame like this:

```python
from whatsappy import get_all_lines, parse_lines_into_df
lines = get_all_lines('path/to/your/file.txt')
df = parse_lines_into_df(lines)
```

now go do some analysis.