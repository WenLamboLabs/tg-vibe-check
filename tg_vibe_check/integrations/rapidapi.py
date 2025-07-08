import os
import time
from typing import Dict
from typing import List

import requests
import streamlit as st


def get_tg_messages(channel: str, limit: int = 50, max_id: int = 999999999) -> List[Dict[str, str]]:
	"""Get messages from a Telegram channel using RapidAPI."""

	try:
		api_key = st.secrets['RAPID_API']
	except KeyError:
		# Fallback to environment variable for local development without secrets.toml
		api_key = os.getenv('RAPID_API')
		if not api_key:
			raise ValueError('RAPID_API not found in st.secrets or environment variables')

	url = 'https://telegram-channel.p.rapidapi.com/channel/message'

	querystring = {'channel': channel, 'limit': str(limit), 'max_id': str(max_id)}

	headers = {'x-rapidapi-key': api_key, 'x-rapidapi-host': 'telegram-channel.p.rapidapi.com'}

	response = requests.get(url, headers=headers, params=querystring)
	response.raise_for_status()

	messages = response.json()

	return [
		{'id': message['id'], 'date': message['date'], 'text': message['text'], 'views': message['views']}
		for message in messages
	]


def get_tg_messages_bulk(channel: str, batch_size: int = 4) -> List[Dict[str, str]]:
	"""Get multiple batches of messages from a Telegram channel using RapidAPI."""

	all_messages = []
	current_max_id = 999999999

	for i in range(batch_size):
		if i > 0:
			time.sleep(1)  # 1 req/s limit

		batch = get_tg_messages(channel, 50, current_max_id)
		if not batch:
			break

		all_messages.extend(batch)
		current_max_id = int(min(message['id'] for message in batch)) - 1

	return all_messages
