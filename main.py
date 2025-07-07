from llm import analyze_tg_vibe
from rapidapi import get_tg_messages

if __name__ == '__main__':
	try:
		# using virtuals channel from t.me/virtuals
		messages = get_tg_messages('virtuals')
		print(f'Retrieved {len(messages)} messages')

		if messages:
			print('First message:')
			print(messages[0])

			print('\nAnalyzing vibe...')
			analysis = analyze_tg_vibe(messages)
			print('Vibe analysis results:')
			print(analysis)
	except Exception as e:
		print(f'Error: {e}')
