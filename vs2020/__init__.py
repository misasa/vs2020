from PIL import Image
import imghdr
import os
import sys
import hashlib
import yaml
import socket
from os.path import expanduser

config_path = os.path.join(expanduser("~"),'.vs2020rc')

default_config = {
		'vsdata_path': 'Z:\\',
		'world_origin': 'ld',
		'stage_origin': 'ru',
		'stage_name': 'stage-of-' + socket.gethostname(),
		'mqtt_host': 'database.misasa.okayama-u.ac.jp',
		'mqtt_port': 1883,
		'tcp_host': '127.0.0.1',
		'tcp_port': '25252',
		'timeout': 5000,
}

def config():
	config = default_config
	try:
		print("reading |%s| ..." % config_path, file=sys.stderr)
		with open(config_path, 'r') as yml:
			config.update(yaml.safe_load(yml))
	except Exception as e:
		print('Exception occurred while loading |%s|...' % config_path, file=sys.stderr)
		print(e, file=sys.stderr)
		try:
			print("writing |%s| ..." % config_path, file=sys.stderr)
			with open(config_path, 'w') as yml:
				yaml.safe_dump(config, yml)
		except Exception as e:
			print('Exception occurred while writing |%s|...' % config_path, file=sys.stderr)
			print(e, file=sys.stderr)
	return config

