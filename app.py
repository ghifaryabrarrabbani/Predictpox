from flask import Flask, render_template, request
import tensorflow as tf
# from keras.models import load_model
import numpy as np
from joblib import load
from PIL import Image
import pandas as pd
import os
import base64
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'GET':
        return render_template('predict.html')
    elif request.method == 'POST':
        model_cnn = tf.keras.models.load_model('mp.h5')
        model_random_forest = load('random_forest_model2.joblib')
        sistemik = request.form['sistemik']
        Swollen_Lymph_Nodes = 0
        Muscle_Aches_and_Pain = 0
        Fever = 0
        if sistemik == '1':
            Swollen_Lymph_Nodes = 1
        elif sistemik == '2':
            Muscle_Aches_and_Pain = 1
        else:
            Fever = 1
        Rectal_pain =request.form['dubur']
        Sore_throat =request.form['tenggorokan']
        Penile_edima =request.form['penis']
        Oral_lesions =request.form['lesi_mulut']
        Solitary_lesions =request.form['lesi_soliter']
        Swollen_tonsils =request.form['amandel']
        HIV_infection =request.form['HIV']
        Sexually_transmitted_infections =request.form['kelamin']
        # # Mengonversi data ke dalam dictionary
        data = pd.DataFrame({
            'Swollen_Lymph_Nodes': [Swollen_Lymph_Nodes],
            'Muscle_Aches_and_Pain': [Muscle_Aches_and_Pain],
            'Fever': [Fever],
            'Rectal_pain': [Rectal_pain],
            'Sore_throat': [Sore_throat],
            'Penile_edema': [Penile_edima],
            'Oral_lesions': [Oral_lesions],
            'Solitary_lesions': [Solitary_lesions],
            'Swollen_tonsils': [Swollen_tonsils],
            'HIV_infection': [HIV_infection],
            'Sexually_transmitted_infections': [Sexually_transmitted_infections]
        })
        gambar = request.files['gambar']
        image_path = request.form['hidden-data-uri']
        # return render_template('bismillah.html',Rectal_pain=Rectal_pain,Swollen_Lymph_Nodes=Swollen_Lymph_Nodes,
        #                         Muscle_Aches_and_Pain=Muscle_Aches_and_Pain,Fever=Fever, Sore_throat=Sore_throat,
        #                         Penile_edima=Penile_edima,Oral_lesions=Oral_lesions,Solitary_lesions=Solitary_lesions,
        #                         Swollen_tonsils=Swollen_tonsils,HIV_infection=HIV_infection,Sexually_transmitted_infections=Sexually_transmitted_infections,
        #                         data=data, image_path=image_path, gambar=gambar)
        if not image_path and not gambar:
            rf_predictions=model_random_forest.predict_proba(data)
            if rf_predictions[0][0] > 0.5:
                total = f"{rf_predictions[0][0] * 100:.2f}%"
                final = "Monkey Pox"
                hasil = f"Prediksi {rf_predictions[0][0] * 100:.2f}% mengalami penyakit {final}"
                return render_template('result2_1.html', message=hasil, total=total)
            else:
                total = f"{rf_predictions[0][0] * 100:.2f}%"
                final = "Monkey Pox"
                hasil = f"Prediksi {rf_predictions[0][0] * 100:.2f}% tidak mengalami penyakit {final}."
                return render_template('result2.html', message=hasil, total=total)
        elif not image_path and gambar:
                    image = Image.open(gambar)
                    img = image.resize((300,300))
                    img = img.convert('RGB')
                    img_array = np.array(img)
                    img_array = np.expand_dims(img_array, axis=0)
                    cnn_predictions = model_cnn.predict(img_array)
                    rf_predictions=model_random_forest.predict_proba(data)
                    if cnn_predictions[0][0] > 0.5:
                        total2 = rf_predictions[0][0] * 100
                        total = cnn_predictions[0][0] * 100
                        final = "Monkey Pox"
                        hasil_total =  f"{total:.2f}%"
                        hasil_total2 =  f"{total2:.2f}%"
                        hasil = f"Prediksi {hasil_total} mengalami penyakit {final}."
                        return render_template('result.html',total=hasil_total,message=hasil,total2=hasil_total2)
                    else:
                        if rf_predictions[0][0] > 0.5:
                            total = f"{cnn_predictions[0][0] * 100:.2f}%"
                            final = "Monkey Pox"
                            total2 = f"{rf_predictions[0][0] * 100:.2f}%"
                            hasil = f"Prediksi {rf_predictions[0][0] * 100:.2f}% mengalami penyakit {final}."
                            return render_template('resultimg.html',total=total,message=hasil,total2=total2)
                        else:
                            final = "Monkey Pox"
                            total = f"{cnn_predictions[0][0] * 100:.2f}%"
                            total2 = f"{rf_predictions[0][0] * 100:.2f}%"
                            hasil = f"Prediksi {rf_predictions[0][0] * 100:.2f}% tidak mengalami penyakit {final} o"
                            return render_template('result3.html',total=total,message=hasil,total2=total2)
        elif not gambar and image_path:
                encoded_data = image_path.split(',')[1]
                decoded_image = base64.b64decode(encoded_data)
                image = Image.open(io.BytesIO(decoded_image))
                image = image.resize((300,300))
                img = image.convert('RGB')
                img_array = np.array(img)
                img_array = np.expand_dims(img_array, axis=0)
                cnn_predictions = model_cnn.predict(img_array)
                rf_predictions=model_random_forest.predict_proba(data)
                if cnn_predictions[0][0] > 0.5:
                    total2 = f"{rf_predictions[0][0] * 100:.2f}%"
                    total = f"{cnn_predictions[0][0] * 100:.2f}%"
                    final = "Monkey Pox"
                    hasil = f"Prediksi {total} mengalami penyakit {final}"
                    return render_template('result.html',total=total,message=hasil,total2=total2)
                else:
                    if rf_predictions[0][0] > 0.5:
                        total = f"{cnn_predictions[0][0] * 100:.2f}%"
                        final = "Monkey Pox"
                        total2 = f"{rf_predictions[0][0] * 100:.2f}%"
                        hasil = f"Prediksi {total} mengalami penyakit {final}"
                        return render_template('resultimg.html',total=total,message=hasil,total2=total2)
                    else:
                        final = "Monkey Pox"
                        total = f"{cnn_predictions[0][0] * 100:.2f}%"
                        total2 = f"{rf_predictions[0][0] * 100:.2f}%"
                        hasil = f"Prediksi {cnn_predictions[0][0] * 100:.2f}% tidak mengalami penyakit {final}"
                        return render_template('result3.html',total=total,message=hasil,total2=total2)
        else:
            return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
# @app.route('/photo')
# def photo():
#     return render_template('coba.html')

# from flask import redirect, url_for
# @app.route('/_photo_cap', methods=['GET','POST'])
# def photo_capture():
#     if request.method == 'GET':
#         return render_template('coba.html')
#     elif request.method == 'POST':
#         data_uri = request.json['photo_cap']

#         # Dekode data URI menjadi gambar
#         encoded_data = data_uri.split(',')[1]
#         decoded_image = base64.b64decode(encoded_data)

#         # Ubah gambar yang telah didekode ke format yang dapat digunakan oleh model ML
#         image = Image.open(io.BytesIO(decoded_image))
#         img = image.resize((300, 300))
#         img = img.convert('RGB')

#         # Konversi gambar menjadi array menggunakan keras.preprocessing.image
#         img_array = keras_image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)

#         # Memuat model dan melakukan prediksi
#         model_path = "C:/Users/Ghifary/OneDrive/Documents/Kuliah/Semester 5/Alpro 2/UAS/.venv/mp.h5"
#         model_cnn = tf.keras.models.load_model(model_path)
#         cnn_predictions = model_cnn.predict(img_array)
#         total = cnn_predictions[0][0] * 100

#         # Mengembalikan respons atau menyimpan hasil prediksi
#         return redirect(url_for('display_result', total=total))
#     else:
#         return '404'

# @app.route('/display_result')
# def display_result():
#     total = request.args.get('total', default=0, type=float)
#     return render_template('hahaha.html', total=total)



