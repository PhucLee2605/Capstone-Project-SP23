from flask import request, Blueprint, render_template, flash, redirect, send_file
from .applications.features.speech_translation import preprocess, model
import os
import torch


views = Blueprint('views', __name__)

pretemp = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
TEMP_TXT_FILE = pretemp + '/static/temp.txt'

if torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/translate')
def translate():
    return render_template("translate.html")

@views.route('/translate', methods=['POST'])
def upload_audio():
    if request.method == "POST":
        file = request.files['text_file']

    if file.filename.endswith('.txt'):
        text = file.read().decode("utf-8")
    elif file.filename.endswith('.xml'):
        text = preprocess.extractXml(file.read().decode("utf-8"))
    else:
        flash('No file selected for uploading')
        return(redirect(request.url))

    #Infer
    tok, mod = model.backBone()
    result = model.infer([['test', 'en: ' + text, '']], tok, mod, 256, DEVICE)

    #Write result to temp file
    with open(TEMP_TXT_FILE, 'w', encoding="utf-8") as f:
        f.write(result[0][0])

    return render_template("translate.html", relink=f'/download/{TEMP_TXT_FILE}')

@views.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)