import os
import time
import win32gui
import win32con
import pyautogui
import subprocess
from pywinauto.application import Application
import pyperclip

# ウィンドウタイトルを設定
WINDOW_TITLE_PARTIAL = "KING OF TIME TIMERECORDER"  # 例: 実際のウィンドウタイトルに含まれる文字列に置き換えてください
MAX_WAIT_SECONDS = 60  # 最大待機時間
app_path = r'C:\Users\Gy488chester-PC\AppData\Local\Apps\2.0\5DD15YQT.PER\8CL6ZTQY.PTX\desk..tion_7a102ef0903acef4_0001.0001_b85bc004edd87f3f\DeskTopTimerecorder.exe'


def launch_and_activate_app(title_part, max_wait):
    """
    アプリを起動し、ウィンドウがアクティブになるのを待ち、アクティブ化します。
    """
    print(f"アプリケーションを起動中: {app_path}")

    # 1. アプリを起動 (非同期)
    # shell=Trueはセキュリティリスクがあるため通常は避けるべきですが、
    # シンプルな起動には便利です。安全性を高めるにはリスト形式で引数を渡します。
    process = subprocess.Popen(app_path, shell=True)

    start_time = time.time()
    hwnd = None

    print(f"ウィンドウが表示されるのを最大 {max_wait} 秒待ちます...")

    # 2. ウィンドウの検出と待機 (ポーリング)
    while time.time() - start_time < max_wait:
        # ウィンドウの列挙とタイトルによる検索
        def find_window_callback(check_hwnd, extra):
            nonlocal hwnd
            # ウィンドウタイトルを取得
            window_text = win32gui.GetWindowText(check_hwnd)
            # ウィンドウが表示されているか、特定のタイトルを含んでいるかを確認
            if window_text and title_part in window_text and win32gui.IsWindowVisible(check_hwnd):
                # ウィンドウのクラス名や他のプロパティでもフィルタリングを強化できます
                hwnd = check_hwnd
                return False  # 列挙を停止
            return True  # 列挙を続行

        win32gui.EnumWindows(find_window_callback, None)

        if hwnd:
            break

        time.sleep(1)  # 1秒待機してから再チェック

    if hwnd is None:
        print(f"エラー: {max_wait} 秒以内にウィンドウが見つかりませんでした。")
        return False
        # 起動したプロセスを終了させるかどうかの処理を検討
        # try:
        #     process.terminate()
        # except:
        #     pass
        # return False

    print(f"ウィンドウが見つかりました (hWnd: {hwnd})。アクティブ化しています。")

    # 3. ウィンドウをアクティブ化

    # ウィンドウが最小化されていたら元に戻す (任意)
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.5)  # 復元後に少し待機

    # 最前面に移動してアクティブ化
    try:
        win32gui.SetForegroundWindow(hwnd)
        # 必要に応じて最大化
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        print("アクティブ化に成功しました。")

    except Exception as e:
        print(f"アクティブ化に失敗しました: {e}")
        return False

    # 待機時間（失敗時のセーフティ）
    pyautogui.PAUSE = 1
    # 画面左上隅にマウスを移動させると強制終了
    pyautogui.FAILSAFE = True

    # path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'souzoku', 'assets', 'png', 'shukkin_button.png')
    path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'souzoku', 'assets', 'png', 'taikin_button.png')
    time.sleep(.5)
    button_location = pyautogui.locateOnScreen(path)

    if button_location is not None:
        # 見つかったボタンの中央をクリック
        pyautogui.click(button_location)
        print("出勤ボタンをクリックしました。")
        time.sleep(1)

        # for _ in range(5):
        #     pyautogui.press('tab')
        #     time.sleep(.2)

        path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'souzoku', 'assets', 'png',
                            'simei_sentaku.png')
        time.sleep(.5)
        button_location = pyautogui.locateOnScreen(path)

        if button_location is not None:
            # 見つかったボタンの中央をクリック
            pyautogui.click(button_location)

            pyperclip.copy('森町 翼')
            time.sleep(.2)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(.2)

            pyautogui.press('tab')
            time.sleep(.1)
            pyperclip.copy('XX@ZjKt49DuY')
            pyautogui.hotkey('ctrl', 'v')

            path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'souzoku', 'assets', 'png',
                                'ninsyou.png')
            button_location = pyautogui.locateOnScreen(path)
            if button_location is not None:
                pyautogui.click(button_location)

        # path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'souzoku', 'assets', 'png',
        #                     'simei_sentaku.png')
        # time.sleep(1)
        # button_location = pyautogui.locateOnScreen(path)
        #
        # if button_location is not None:
        #     pyautogui.click(button_location)
        #     print("氏名選択ボタンをクリックしました。")
        #     time.sleep(2)
        #
        #     print("下にスクロールします。")
        #     pyautogui.scroll(-100)
        #
        #     time.sleep(2)
        #     print("↑にスクロールします。")
        #     pyautogui.scroll(100)
        #
        #     path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'souzoku', 'assets', 'png',
        #                         'simei.png')
        #     time.sleep(1)
        #     button_location = pyautogui.locateOnScreen(path)
        #
        #     if button_location is not None:
        #         pyautogui.click(button_location)
        #         print("氏名ボタンをクリックしました。")
        #         time.sleep(.5)
        #
        #         pyautogui.press('tab')
        #         time.sleep(.1)
        #         pyperclip.copy('XX@ZjKt49DuY')  # 文字列をクリップボードにコピー
        #         pyautogui.hotkey('ctrl', 'v')  # Ctrl+V で貼り付け

    else:
        print("ボタンの画像が画面に見つかりませんでした。")

    return True


# 実行
launch_and_activate_app(WINDOW_TITLE_PARTIAL, MAX_WAIT_SECONDS)