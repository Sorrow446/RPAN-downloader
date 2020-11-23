# RPAN-downloader
Tool written in Python to download Reddit Public Access Network VODs.

# Setup
Put FFmpeg binary in the script's directory.

# Usage
Download two streams to default directory:  
`rpan_downloader.py -u https://www.reddit.com/rpan/r/RedditSessions/jypyug https://www.reddit.com/rpan/r/RedditSessions/jtazrp`

Download from text file to "G:\":  
`rpan_downloader.py -u E:\links.txt -o G:\`
```
usage: rpan_downloader.py [-h] -u URLS [URLS ...] [-t TEMPLATE] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -u URLS [URLS ...], --urls URLS [URLS ...]
                        Multiple URLs or a text file filename / abs path.
  -t TEMPLATE, --template TEMPLATE
                        Naming template for filenames.
  -o OUTPUT, --output OUTPUT
                        Output path.
``` 
