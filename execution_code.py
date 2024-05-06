import asyncio
import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from flask import Flask, request, render_template, jsonify, make_response
import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps
from flask import send_file
from flask import request


app = Flask(__name__)

#使用するカメラ番号(example innercamera=0 outsidecamera=1)
camera_number=0

#背景白化画像の生成
def highlight_image_difference(image_path_a, image_path_b, output_path, threshold=30):
    # 画像を読み込む
    image_a = cv2.imread(image_path_a)
    image_b = cv2.imread(image_path_b)

    # 画像のサイズが異なる場合はエラーを出力
    if image_a.shape != image_b.shape:
        raise ValueError("Images must be the same size")

    # 差分画像を計算
    diff = cv2.absdiff(image_a, image_b)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # 閾値を適用して差分を強調
    _, thresholded = cv2.threshold(diff_gray, threshold, 255, cv2.THRESH_BINARY)

    # マスクを生成
    mask = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)

    # 差異がない部分を白色にする
    new_image = np.where(mask == 255, image_b, (192,192,192))#white(255, 255, 255))


    # 画像を保存
    cv2.imwrite(output_path, new_image)


# カメラデバイスのキャプチャ
cap = cv2.VideoCapture(camera_number)

# カメラが正しく開かれたかどうかを確認
if not cap.isOpened():
    print("Error: Unable to open camera.")
    exit()

# 画像を保存するディレクトリとファイル名のプレフィックス
output_directory = "folder_path" #ここに画像を保存するディレクトリパスを入力
file_prefix = 'image'

# ファイル番号
file_number = 1

# 15枚の写真を撮る
for i in range(15):
    # フレームをキャプチャ
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break
    

    
    # ファイルに保存
    filename = output_directory + file_prefix + str(file_number) + '.jpg'
    cv2.imwrite(filename, frame)
    print("Image saved as", filename)
    
    # ファイル番号を更新
    file_number += 1
    

# カメラを解放
cap.release()

#10～15枚目の平均画像の生成
# 画像の読み込み
images = []
for i in range(11, 16):
    image = cv2.imread(f"image{i}.jpg")
    images.append(image)

# 画像のサイズを取得
height, width, channels = images[0].shape

# 画像の平均を計算
average_image = np.zeros((height, width, channels), dtype=np.float32)
for image in images:
    average_image += image / len(images)

# 平均画像を保存
cv2.imwrite("average_image.jpg", average_image)
print('average_image')

gmail_address = None
error_count = 0

#モデルのパス指定
model = load_model(r"keras_model2.h5", compile=False)
class_names = open(r"labels.txt", "r", encoding="utf-8").readlines()

camera = cv2.VideoCapture(camera_number)

paused = False

async def detect_error(gmail_address):
    global error_count

    while True:  # 無限ループ
        if paused:
            await asyncio.sleep(0.5)  # 0.5秒待機
            continue

        filename = await take_photo()
        class_name = await process_image(filename)
        print("Class:", class_name[2:])
        response = make_response(jsonify({"result": class_name, "image_path": filename}))
        yield response

        if class_name[2:] == '状態異常':
            error_count += 1
            print('状態異常')
            print(error_count)
            
            if error_count == 20:
                await send_email(gmail_address, filename)
                error_count = 0

        else:
            error_count = 0
            print('異常なし')
            print(error_count)


async def take_photo(filename='input_photo.jpg'):
    return_value, image = camera.read()
    cv2.imwrite(filename, image)
    filename="photo.jpg"
    highlight_image_difference("average_image.jpg", "input_photo.jpg", "photo.jpg")
    print('リアルタイム写真')
    
    return filename

async def process_image(filename):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(filename).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
   
    return class_name

async def send_email(receiver_email, filename):
    filename = 'input_photo.jpg'
    sender_email = 'your_email@gmail.com' #送信元のgmailメールアドレスを設定
    password = 'your_password' #アプリパスワード入力

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = '異常検知'

    body = MIMEText('異常を検知しました')
    msg.attach(body)

    img_data = open(filename, 'rb').read()
    image = MIMEImage(img_data, name='異常検知.jpg')
    msg.attach(image)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print(receiver_email, 'にメールが送信されました。')


@app.route('/')
def home():
    return render_template('index.html', result=None, image_path=None)
   
@app.route('/detect_error', methods=['POST'])
async def detect_error_route():
    global gmail_address
    gmail_address = request.form['gmail_name']
    return await asyncio.gather(*[response async for response in detect_error(gmail_address)])
    
@app.route('/get_data')
async def get_data():
    image_path = 'photo.jpg'
    class_name = await process_image(image_path)
    return jsonify(class_name=class_name)

@app.route('/photo')
async def get_photo():
    return await asyncio.to_thread(send_file, 'photo.jpg', mimetype='image/jpeg')

@app.route('/toggle_execution', methods=['POST'])
def toggle_execution():
    global paused
    paused = not paused
    return "Execution paused" if paused else "Execution resumed"



if __name__ == "__main__":
    app.run(host="0.0.0.0")
