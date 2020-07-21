import subprocess
from time import sleep

import pyautogui


XSEL_PATH = r"C:\Program Files (x86)\IAI\X_SEL\X_SEL.exe"

class XselController:
    def __init__(self):
        # launch xsel if not yet
        icon_p = self.locate_png_element(r'png/xsel_icon.png')
        if icon_p is None:
            print("Launching xsel ...")
            subprocess.Popen(XSEL_PATH)
            while (self.locate_png_element(r'png/err_228_callendar.png') is None) and \
                (self.locate_png_element(r'png/err_c6e_servo.png') is None):
                sleep(1)
            pyautogui.click(1924, 1138) # click cancel button
            print("Launched sucessfully !!")

    # ポジションのエディターを開く関数
    def open_position_editor(self):
        self.move_window_to_right()
        if self.locate_png_element(r'png/position_data_edit.png') is not None or \
            self.locate_png_element(r'png/position_data_edit2.png') is not None:
            print('Position editor is already opened')
            return 0
        
        pb_x, pb_y = self.locate_png_element(r'png/position_button.png')
        pyautogui.click(pb_x, pb_y)           # ポジションボタンをクリック
        sleep(0.1)
        pyautogui.click(pb_x, pb_y+30)        # 編集ボタンをクリック。
        sleep(0.2)
        ob_x, ob_y = self.locate_png_element(r'png/ok_button.png') # OKボタンを検索
        sleep(0.1)
        pyautogui.click(ob_x, ob_y)           # OKボタンをクリック
        sleep(0.2)
        bfs_x, bfs_y = self.locate_png_element(r'png/blue_full_screen_button.png')
        sleep(0.2)
        pyautogui.click(bfs_x, bfs_y)         # エディターを全画面表示にする

    # pyautoguiのlocateCenerOnScreenのラッパー
    def locate_png_element(self, png_file_path):
        return pyautogui.locateCenterOnScreen(
            png_file_path,
            grayscale=True,
            confidence=0.9,
        )

    # xselアプリを最前面に持ってくる関数
    def move_window_to_front(self):
        i_x, i_y = self.locate_png_element(r'png/xsel_icon.png')
        pyautogui.click(i_x, i_y)
        if self.locate_png_element(r'png/position_button.png') is None:
            pyautogui.click()
            sleep(0.1)
        pyautogui.moveRel(-100, -100)

    # xselアプリを右に配置する関数
    def move_window_to_right(self):
        self.move_window_to_front()
        pyautogui.keyDown('winleft')
        pyautogui.keyDown('up')
        pyautogui.keyUp('up')
        sleep(0.1)
        pyautogui.keyDown('right')
        pyautogui.keyDown('esc')
        pyautogui.keyUp('winleft')
        pyautogui.keyUp('right')
        pyautogui.keyUp('esc')

    # servoをオンにする関数
    def on_servo_motor(self):
        self.move_window_to_right()
        if self.locate_png_element(r'png/sv_hm_mv_buttons__sv_on.png') is not None:
            print('Servo motors are already on')
            return 0
        print("Please Cancel the Emergency Mode")
        input("Release the Button and input Enter: ")
        shmb_ps = self.get_svhmmv_buttom_points()
        sleep(0.1)
        pyautogui.click(shmb_ps['x_sv_x'], shmb_ps['y'])
        pyautogui.click(shmb_ps['y_sv_x'], shmb_ps['y'])
        pyautogui.click(shmb_ps['z_sv_x'], shmb_ps['y'])
    
    # SVOFFSV, HM, MVのボタンの座標を取得する関数
    def get_svhmmv_buttom_points(self):
        self.move_window_to_right()
        shmb_x, shmb_y = self.locate_png_element(r'png/vel_mm_sec.png')
        return {
            'y':shmb_y,
            'x':shmb_x,
            'x_sv_x':shmb_x - 436,
            'x_hm_x':shmb_x - 395,
            'x_mv_x':shmb_x - 369,
            'y_sv_x':shmb_x - 294,
            'y_hm_x':shmb_x - 255,
            'y_mv_x':shmb_x - 231,
            'z_sv_x':shmb_x - 144,
            'z_hm_x':shmb_x - 104,
            'z_mv_x':shmb_x - 79,
        }

    def move_to_home_position(self):
        self.move_window_to_right()
        shmb = self.get_svhmmv_buttom_points()
        sleep(0.1)
        pyautogui.click(shmb['x_hm_x'], shmb['y'])
        pyautogui.click(shmb['y_hm_x'], shmb['y'])
        pyautogui.click(shmb['z_hm_x'], shmb['y'])

    def move_to_x_y_z(self, x, y, z):
        if x < 1 or x > 300:
            raise ValueError('x must be 1 - 300')
        if y < 1 or y > 249:
            raise ValueError('y must be 1 - 249')
        if z < 1 or z > 100:
            raise ValueError('z must be 1 - 100')
        shmb = self.get_svhmmv_buttom_points()

        nn1_x, nn1_y = self.locate_png_element(r'png/no_name_1.png') # Point(x=2781, y=323)        
        axis1_x = nn1_x + 119
        column1 = nn1_y + 25

        pyautogui.click(axis1_x, column1)
        pyautogui.press('up', presses=350) # 左上が0.000になるようにする。
        pyautogui.press('left', presses=4) # 左上が0.000になるようにする。
        
        pyautogui.press('down', presses=x)
        pyautogui.click(shmb['x_mv_x'], shmb['y'])
        sleep(0.5)
        while self.locate_png_element(r'png/moving.png') is not None:
            sleep(0.1)
        pyautogui.click(3603, 754)
        pyautogui.press('up')
        pyautogui.press('up', presses=x)
        pyautogui.press('right')

        pyautogui.press('down', presses=y)
        pyautogui.click(shmb['y_mv_x'], shmb['y'])
        sleep(0.5)
        while self.locate_png_element(r'png/moving.png') is not None:
            sleep(0.1)
        pyautogui.click(3603, 754)
        pyautogui.press('up')
        pyautogui.press('up', presses=y)
        pyautogui.press('right', presses=2)
        
        pyautogui.press('down', presses=z)
        pyautogui.click(shmb['z_mv_x'], shmb['y'])
        sleep(0.5)
        while self.locate_png_element(r'png/moving.png') is not None:
            sleep(0.1)
        pyautogui.press('up')
        pyautogui.press('up', presses=z)
        sleep(0.5)

if __name__=="__main__":
    xc = XselController()
    xc.open_position_editor()
    xc.on_servo_motor()
    xc.move_to_x_y_z(1, 1, 1)
    xc.move_to_x_y_z(100, 100, 50)
    xc.move_to_x_y_z(300, 249, 100)

    # xc.move_to_home_position()
    # while True:
    #     print(pyautogui.position())
    
