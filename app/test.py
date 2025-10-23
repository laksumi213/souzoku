import pytesseract
from PIL import Image
import pandas as pd  # 結果をデータフレームとして扱うため

# 1. Tesseractの実行ファイルのパスを設定（Windowsユーザー向け）
# 🚨 注意: Tesseractをインストールした場所に合わせてパスを変更してください
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 2. 画像ファイルを読み込む
# 🚨 注意: 'input_document.png' を実際のファイル名に置き換えてください
try:
    img = Image.open('input_document.png')
except FileNotFoundError:
    print("エラー: 'input_document.png' が見つかりません。ファイル名を確認してください。")
    exit()

# 3. 座標情報を含むOCR結果を取得
# output_type.DATAFRAME を指定することで、結果がデータフレームとして返されます
data = pytesseract.image_to_data(
    img,
    lang='jpn',  # 認識言語を日本語に設定
    output_type=pytesseract.Output.DATAFRAME
)

# 4. 認識結果と座標情報を表示
print("--- データフレームの最初の5行 ---")
print(data.head())

# 5. 必要な情報（認識された単語とその座標）を抽出
# 'level' 5 は通常、認識された「単語」を指します
words_data = data[data.conf != -1]  # 信頼度（conf）が-1でない行（認識された行）のみを抽出
words_data = words_data[words_data.text.str.strip().astype(bool)]  # 空白行を除外

print("\n--- 抽出された単語とその座標 ---")
for index, row in words_data.iterrows():
    text = row['text']
    # 座標情報
    x = row['left']
    y = row['top']
    w = row['width']
    h = row['height']
    conf = row['conf']  # 信頼度 (0-100)

    # 抽出された情報
    print(f"テキスト: {text}, 信頼度: {conf}, 座標 (x, y, w, h): ({x}, {y}, {w}, {h})")