from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        url = data['url']
        output_path = data.get('output_path')

        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        if output_path is None:
            output_path = video_stream.default_filename

        video_stream.download(output_path)

        response = {
            'status': 'success',
            'message': 'Video downloaded successfully',
            'file_path': output_path
        }
    except Exception as e:
        response = {
            'status': 'error',
            'message': f'Error downloading video: {str(e)}'
        }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
