import os
import re
import sys
import argparse
import traceback
import subprocess

import requests


def check_url(url):
	regex = r'https://www.reddit.com/rpan/r/\w{3,21}/(j[a-zA-Z\d]{5})'
	match = re.match(regex, url)
	if match:
		return match.group(1)

def read_txt(abs):
	with open(abs) as f:
		urls = [u.strip() for u in f.readlines()]
	return urls	

def parse_prefs():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-u', '--urls', 
		nargs='+', required=True,
		help='Multiple URLs or a text file filename / abs path.'
	)
	parser.add_argument(
		'-t', '--template', 
		default='{author} - {title}_{id}',
		help="Naming template for filenames."
	)
	parser.add_argument(
		'-o', '--output', 
		default='RPAN downloader downloads',
		help='Output path.'
	)
	args = parser.parse_args()	
	if args.urls[0].endswith('.txt'):
		args.urls = read_txt(args.urls[0])
	return args

def dir_setup():
	if not os.path.isdir(args.output):
		os.makedirs(args.output)

def parse_template(meta):
	del meta['manifest_url']
	try:
		return args.template.format(**meta)
	except KeyError:
		print(
			"Failed to parse filename naming template. Default one "
			"will be used instead."
		)
		return "{author} - {title}_{id}".format(**meta)

def get_meta(stream_id):
	r = session.get('https://strapi.reddit.com/videos/t3_' + stream_id)
	r.raise_for_status()
	json = r.json()
	assert json['status'] == "success", "Got a bad response."
	assert json['data']['stream']['state'] == "ENDED", "Stream is still being streamed."
	assert json['data']['stream']['vod_accessible'] == True, "Stream is inaccessible."
	return {
		'author': json['data']['post']['authorInfo']['name'],
		'title': json['data']['post']['title'],
		'id': stream_id,
		'manifest_url': json['data']['stream']['hls_url'],
	}

def sanitize(f):
	return re.sub(r'[\/:*?"><|]', '_', f)	
	
def main(stream_id):
	print("Getting metadata...")
	meta = get_meta(stream_id)
	print(meta['author'] + " - " + meta['title']) 
	manifest_url = meta['manifest_url']
	abs = os.path.join(args.output, sanitize(parse_template(meta)) + ".mp4")
	if os.path.isfile(abs):
		print("Stream already exists locally.")
		return
	print("Calling FFmpeg...")
	subprocess.run(['ffmpeg', '-i', manifest_url, '-map', '0:p:0', '-c', 'copy', abs])

if __name__ == '__main__':
	try:
		if hasattr(sys, 'frozen'):
			os.chdir(os.path.dirname(sys.executable))
		else:
			os.chdir(os.path.dirname(__file__))
	except OSError:
		pass
	assert os.path.isfile('ffmpeg.exe'), "FFmpeg binary is missing."
	session = requests.Session()
	session.headers.update({
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
					  '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
	})
	args = parse_prefs()
	total = len(args.urls)
	dir_setup()
	for num, url in enumerate(args.urls, 1):
		print("\nURL {} of {}:".format(num, total))
		stream_id = check_url(url)
		if stream_id == None:
			print("Invalid url:", url)
			continue
		try:
			main(stream_id)
		except Exception:
			print("URL failed.")
			traceback.print_exc()