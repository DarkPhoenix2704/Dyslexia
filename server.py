import io
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import wave
import pickle as pkl
import speech_recognition as sr
import eng_to_ipa as ipa
import soundfile
import os


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model = pkl.load(open("./ml-model/model.pkl", 'rb'))


def isDyslexic(inaccuracy, time):
    prediction = model.predict([[inaccuracy, time]])[0]
    if prediction == 0:
        return False
    else:
        return True


def predict(audio):
    text = listen_for(audio)
    print(text)
    return text


def listen_for(source):
    r = sr.Recognizer()
    with sr.AudioFile(source) as source:
        audio = r.record(source)  # read the entire audio file
        text = r.recognize_google(audio)
        return text


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # j+1 instead of j since previous_row and current_row are one character longer
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def check_pronounciation(str1: str, str2: str):
    s1 = ipa.convert(str1)
    s2 = ipa.convert(str2)
    return levenshtein(s1, s2)


@app.route('/', methods=['POST'])
@cross_origin()
def main():
    f = request.files['file']
    seconds = request.form['seconds']
    string_displayed = request.form['string_displayed']

    f.save('temp.opus')
    f.seek(0)
    os.system(f'ffmpeg -i "temp.opus" -vn "temp.wav"')

    os.remove('temp.opus')

    string_pronounced = predict("temp.wav")

    pronounciation_inaccuracy = check_pronounciation(
        string_displayed, string_pronounced)/len(string_displayed)

    result = isDyslexic(pronounciation_inaccuracy, seconds)
    os.remove('temp.wav')

    return jsonify({"isDyslexic": result, "pronounciation_inaccuracy": pronounciation_inaccuracy})


if __name__ == '__main__':
    app.run(debug=False, port=5000)
