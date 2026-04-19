from flask import Flask, jsonify, request
import yt_dlp
import os

app = Flask(__name__)

API_KEY = os.environ.get('API_KEY')

@app.route('/audio', methods=['GET'])
def get_audio_url():
    key = request.headers.get('X-Api-Key')
    if API_KEY and key != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401

    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400

    try:
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios'],  # iOS client bypasses bot detection
                }
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            title     = info.get('title', '')
            duration  = info.get('duration', 0)

            return jsonify({
                'audio_url': audio_url,
                'title': title,
                'duration': duration
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)