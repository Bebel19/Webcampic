from flask import Flask, send_from_directory, render_template, redirect, url_for, Response
import cv2
from flask_bootstrap import Bootstrap
import os
import subprocess

app = Flask(__name__)
Bootstrap(app)

# Assurez-vous que ce chemin pointe vers le dossier où vous enregistrez les images capturées
DOSSIER_IMAGES = os.path.join('static', 'images')

@app.route('/')
def galerie():
    images = os.listdir(DOSSIER_IMAGES)
    images.sort(reverse=True)
    return render_template('galerie.html', images=images)

@app.route('/images/<nom>')
def image(nom):
    return send_from_directory(DOSSIER_IMAGES, nom)

@app.route('/capture', methods=['POST'])
def capture():
    subprocess.run(['./capture.sh'])
    return redirect(url_for('galerie'))

# Initialisation de la capture vidéo
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L) 

def generate_video_feed():
    while True:
        success, frame = cap.read()  # Lecture de la frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Route pour servir le flux vidéo généré."""
    return Response(generate_video_feed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='192.168.1.166', port=8080, debug=True, threaded=True)
