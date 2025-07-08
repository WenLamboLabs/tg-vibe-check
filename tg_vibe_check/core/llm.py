import json
from typing import Dict
from typing import List

from bs4 import BeautifulSoup
from litellm import completion

from tg_vibe_check.core.prompt import PROMPT


def analyze_tg_vibe(messages: List[Dict[str, str]], model: str = 'anthropic/claude-sonnet-4-20250514') -> Dict:
	"""Analyze Telegram messages to generate a crypto community vibe check report."""

	formatted_messages = [{'date': msg['date'], 'text': msg['text']} for msg in messages]

	prompt_with_messages = PROMPT.replace(
		'{{INSERT JSON ARRAY OF MESSAGES HERE}}', json.dumps(formatted_messages, indent=2)
	)

	llm_messages = [{'role': 'user', 'content': prompt_with_messages}]

	response = completion(
		model=model,
		messages=llm_messages,
		temperature=0.1,
	)

	response_content = response.choices[0].message.content

	# parse the response inside <answer> tags
	soup = BeautifulSoup(response_content, 'html.parser')
	content = soup.find('answer').get_text()
	return json.loads(content)
