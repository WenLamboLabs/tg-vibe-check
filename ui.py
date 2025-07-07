import streamlit as st

from llm import analyze_tg_vibe
from rapidapi import get_tg_messages

# Configure page title and icon
st.set_page_config(page_title='TG Vibe Check', page_icon='🔍')


def get_status_colors(score, good_threshold, bad_threshold, higher_is_better=True):
	"""Get delta value and color based on score and thresholds."""
	if higher_is_better:
		if score >= good_threshold:
			return 'Good', 'normal'
		elif score <= bad_threshold:
			return 'Bad', 'inverse'
		else:
			return 'Moderate', 'off'
	else:
		if score <= good_threshold:
			return 'Good', 'normal'
		elif score >= bad_threshold:
			return 'Bad', 'inverse'
		else:
			return 'Moderate', 'off'


def render_metric(label, value, help_text, good_threshold, bad_threshold, higher_is_better=True, is_integer=False):
	"""Render a metric with status colors."""
	delta_value, delta_color = get_status_colors(value, good_threshold, bad_threshold, higher_is_better)

	value_str = f'{value}' if is_integer else f'{value:.2f}'

	st.metric(
		label=label,
		value=value_str,
		delta=delta_value,
		delta_color=delta_color,
		help=help_text,
		border=True,
	)


# Custom CSS to hide arrows in metrics
st.markdown(
	"""
<style>
div[data-testid="stMetricDelta"] svg {
    display: none;
}
</style>
""",
	unsafe_allow_html=True,
)


def main():
	st.title('TG Vibe Check')
	st.markdown(
		'Read the room before the room reads you. Built by [WenLambo Labs](https://wenl.ai/blog/tg-vibe-check).'
	)

	# 1. Dropdown Selection
	channels = {
		'Virtuals': 'virtuals',
		'Cookie': 'cookie_dao',
		'Bittensor': 'taobittensor',
		'NEAR': 'cryptonear',
		'Render': 'rendernetwork',
		'Hey Anon': 'realwagmi',
	}
	channel_label = st.selectbox(
		'Choose a Telegram channel to analyze:',
		list(channels.keys()),
		index=0,
	)
	channel = channels[channel_label]

	# Analysis button
	if st.button('Start Vibe Check', use_container_width=True):
		# 2. Long-Running Analysis with Progress Tracking
		with st.status('Running vibe check analysis...', expanded=True) as status:
			st.write('📡 Scanning community channel...')
			try:
				messages = get_tg_messages(channel)
				st.write(f'✅ Retrieved {len(messages)} messages')
			except Exception as e:
				st.error(f'❌ Failed to fetch messages: {str(e)}')
				st.stop()

			st.write('🔍 Analyzing sentiment patterns...')
			try:
				results = analyze_tg_vibe(messages)
				st.write('✅ Analysis complete!')
			except Exception as e:
				st.error(f'❌ Analysis failed: {str(e)}')
				st.stop()

			status.update(label='Analysis complete! ⚡', state='complete', expanded=False)

		# 3. Dashboard with Metrics
		display_results(results)


def display_results(results):
	"""Display the analysis results in a dashboard format."""

	# Sentiment & Psychology Metrics
	st.subheader('💭 Sentiment & Psychology')
	col1, col2, col3 = st.columns(3)

	sentiment = results['sentiment_psychology_metrics']

	with col1:
		fud_score = sentiment['fud_coefficient']['score']
		render_metric(
			label='FUD Coefficient',
			value=fud_score,
			help_text='Fear, Uncertainty, Doubt level (0=low, 1=high)',
			good_threshold=0.3,
			bad_threshold=0.7,
			higher_is_better=False,
		)

	with col2:
		cope_score = sentiment['cope_level']['score']
		render_metric(
			label='Cope Level',
			value=cope_score,
			help_text='Unrealistic optimism level (0=realistic, 1=high cope)',
			good_threshold=0.3,
			bad_threshold=0.7,
			higher_is_better=False,
		)

	with col3:
		cohesion_score = sentiment['community_cohesion']['score']
		render_metric(
			label='Community Cohesion',
			value=cohesion_score,
			help_text='Unity and support level (0=divided, 1=unified)',
			good_threshold=0.7,
			bad_threshold=0.3,
			higher_is_better=True,
		)

	# Engagement Quality Indicators
	st.subheader('🎯 Engagement Quality')
	col1, col2, col3 = st.columns(3)

	engagement = results['engagement_quality_indicators']

	with col1:
		moon_score = engagement['moon_boy_density']['score']
		render_metric(
			label='Moon Boy Density',
			value=moon_score,
			help_text='Low-effort hype ratio (0=quality discussion, 1=pure hype)',
			good_threshold=0.3,
			bad_threshold=0.7,
			higher_is_better=False,
		)

	with col2:
		help_score = engagement['helpfulness_ratio']['score']
		render_metric(
			label='Helpfulness Ratio',
			value=help_score,
			help_text='Question answering quality (0=poor support, 1=helpful)',
			good_threshold=0.7,
			bad_threshold=0.3,
			higher_is_better=True,
		)

	with col3:
		signal_score = engagement['signal_to_noise_ratio']['score']
		render_metric(
			label='Signal-to-Noise Ratio',
			value=signal_score,
			help_text='Technical discussion quality (0=noise, 1=signal)',
			good_threshold=0.7,
			bad_threshold=0.3,
			higher_is_better=True,
		)

	# Red Flag Detection
	st.subheader('🚨 Red Flag Detection')
	col1, col2, col3 = st.columns(3)

	red_flags = results['red_flag_detection']

	with col1:
		rugpull_score = red_flags['rugpull_anxiety_index']['score']
		render_metric(
			label='Rugpull Anxiety',
			value=rugpull_score,
			help_text='Number of rugpull concerns (0=none, higher=more concerns)',
			good_threshold=0,
			bad_threshold=1,
			higher_is_better=False,
			is_integer=True,
		)

	with col2:
		bot_score = red_flags['bot_shill_probability']['score']
		render_metric(
			label='Bot/Shill Probability',
			value=bot_score,
			help_text='Likelihood of bot activity (0=organic, 1=heavy bots)',
			good_threshold=0.3,
			bad_threshold=0.7,
			higher_is_better=False,
		)

	with col3:
		desperation_score = red_flags['price_desperation_score']['score']
		render_metric(
			label='Price Desperation',
			value=desperation_score,
			help_text='Obsession with price action (0=patient, 1=desperate)',
			good_threshold=0.3,
			bad_threshold=0.7,
			higher_is_better=False,
		)

	# Detailed Analysis Tabs
	st.markdown('---')

	tab1, tab2, tab3 = st.tabs(['💭 Sentiment Details', '🎯 Engagement Details', '🚨 Red Flag Details'])

	with tab1:
		# FUD Coefficient
		st.markdown('### FUD Coefficient')
		st.write(sentiment['fud_coefficient']['explanation'])
		if sentiment['fud_coefficient']['supporting_messages']:
			for msg in sentiment['fud_coefficient']['supporting_messages']:
				st.markdown(f'> {msg}')

		st.markdown('---')

		# Cope Level
		st.markdown('### Cope Level')
		st.write(sentiment['cope_level']['explanation'])
		if sentiment['cope_level']['supporting_messages']:
			for msg in sentiment['cope_level']['supporting_messages']:
				st.markdown(f'> {msg}')

		st.markdown('---')

		# Community Cohesion
		st.markdown('### Community Cohesion')
		st.write(sentiment['community_cohesion']['explanation'])
		if sentiment['community_cohesion']['supporting_messages']:
			for msg in sentiment['community_cohesion']['supporting_messages']:
				st.markdown(f'> {msg}')

	with tab2:
		# Moon Boy Density
		st.markdown('### Moon Boy Density')
		st.write(engagement['moon_boy_density']['explanation'])
		if engagement['moon_boy_density']['supporting_messages']:
			for msg in engagement['moon_boy_density']['supporting_messages']:
				st.markdown(f'> {msg}')

		st.markdown('---')

		# Helpfulness Ratio
		st.markdown('### Helpfulness Ratio')
		st.write(engagement['helpfulness_ratio']['explanation'])
		if engagement['helpfulness_ratio']['supporting_messages']:
			for msg in engagement['helpfulness_ratio']['supporting_messages']:
				st.markdown(f'> {msg}')

		st.markdown('---')

		# Signal-to-Noise Ratio
		st.markdown('### Signal-to-Noise Ratio')
		st.write(engagement['signal_to_noise_ratio']['explanation'])
		if engagement['signal_to_noise_ratio']['supporting_messages']:
			for msg in engagement['signal_to_noise_ratio']['supporting_messages']:
				st.markdown(f'> {msg}')

	with tab3:
		# Rugpull Anxiety
		st.markdown('### Rugpull Anxiety')
		st.write(red_flags['rugpull_anxiety_index']['explanation'])
		if red_flags['rugpull_anxiety_index']['supporting_messages']:
			for msg in red_flags['rugpull_anxiety_index']['supporting_messages']:
				st.markdown(f'> {msg}')

		st.markdown('---')

		# Bot/Shill Probability
		st.markdown('### Bot/Shill Probability')
		st.write(red_flags['bot_shill_probability']['explanation'])
		if red_flags['bot_shill_probability']['supporting_messages']:
			for msg in red_flags['bot_shill_probability']['supporting_messages']:
				st.markdown(f'> {msg}')

		st.markdown('---')

		# Price Desperation
		st.markdown('### Price Desperation')
		st.write(red_flags['price_desperation_score']['explanation'])
		if red_flags['price_desperation_score']['supporting_messages']:
			for msg in red_flags['price_desperation_score']['supporting_messages']:
				st.markdown(f'> {msg}')


if __name__ == '__main__':
	main()
