# RPAN-downloader
Tool written in Python to download Reddit Public Access Network VODs.

# Setup
Put FFmpeg binary in the script's directory.

# Usage
Download two streams to default directory:  
`rpan_downloader.py -u https://www.reddit.com/rpan/r/RedditSessions/jypyug https://www.reddit.com/rpan/r/RedditSessions/jtazrp`
Download from text file to "G:\":  
`rpan_downloader.py -u E:\links.txt -o G:\`
