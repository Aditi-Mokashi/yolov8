import os
from flask import Flask, request, render_template
from predictWithOcr import predict
from omegaconf import OmegaConf
from pathlib import Path
from db_utils import insert_to_realtime_db

app = Flask(__name__)

DEFAULT_CONFIG = Path("config.yaml")


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/')
# def index():
#     return '''
#     <form method="POST" enctype="multipart/form-data" action="/process_video">
#         <input type="file" name="video">
#         <input type="submit" value="Upload">
#     </form>
#     '''

@app.route('/process_video', methods=['POST'])
def process_video():
    video_file = request.files['video']
    # video_data = video_file.read()  # Read video data
    video_file.save('assets/uploaded_video.mp4')
    video_path = os.path.join(os.getcwd(), "assets", "uploaded_video.mp4")
    # Pass video data to the desired function for processing
    # Get the configuration object
    cfg = OmegaConf.load(DEFAULT_CONFIG)
    # Set the source parameter in the configuration object
    cfg.source = video_path
    # Call the predict function with the modified configuration object
    predict(cfg)

    insert_to_realtime_db()

    return 'Video processed successfully'


if __name__ == '__main__':
    app.run(debug=True)
