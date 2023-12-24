from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from pypresence import Presence
import re
from time import time

app = Flask(__name__)

client_id = 'your client id'
RPC = Presence(client_id)
RPC.connect()

@app.route('/updateRichPresence', methods=['POST'])
def update_rich_presence():
    data = request.get_json()
    handle_update_rich_presence(data)
    return jsonify({'status': 'success', 'message': 'Update successful'})

def handle_update_rich_presence(data):
    html = data.get('html', '')
    soup = BeautifulSoup(html, 'html.parser')
    progress_wrapper = soup.find('div', {'class': 'playbackTimeline__progressWrapper'})
    duration_element = soup.find('div', {'class': 'playbackTimeline__duration'})

    seconds_passed = int(progress_wrapper.get('aria-valuenow', '0'))

    avatar_link_style = soup.select_one('.playbackSoundBadge__avatar span')['style']
    username = soup.select_one('.playbackSoundBadge__lightLink')['title']
    track_title = soup.select_one('.playbackSoundBadge__titleLink')['title']

    link = 'https://soundcloud.com/' + soup.find('a', {'class': 'playbackSoundBadge__titleLink'})['href']

    match = re.search(r'url\("([^"]+)"\)', avatar_link_style)
    avatar_link = match.group(1) if match else ''

    duration_text = duration_element.find('span', {'aria-hidden': 'true'}).get_text()
    minutes, seconds = map(int, duration_text.split(':'))
    total_duration_seconds = minutes * 60 + seconds

    track_data = {
        'title': track_title,
        'user': {'username': username},
        'artwork_url': avatar_link,
        'permalink_url': link,
        'passed': seconds_passed,
        'duration': total_duration_seconds
    }

    send_discord_rpc(track_data)

def send_discord_rpc(track_data):
    start_timestamp = int(time()) - track_data['passed']

    RPC.update(
        details=f'{track_data["title"]}',
        state=f'by {track_data["user"]["username"]}',
        start=start_timestamp,
        end=start_timestamp + track_data['duration'],
        large_image=track_data['artwork_url'] or "https://i.imgur.com/jus7rW5.jpeg",
        large_text='discord rpc by 3j333',
        buttons=[
            {'label': 'Play on Soundcloud', 'url': track_data['permalink_url']}
        ]
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7769)