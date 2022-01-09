import cv2
import pyautogui as pg
import keyboard as kb

from tkinter import *
from tkinter.ttk import *
from time import sleep

from typing import Iterable


alphabet = ["a", "b", "c"]


class Consts:
    WIN_SIZE = "1345x740"
    ENTER_X_SHIFT, ENTER_Y_SHIFT = 40, 155
    FIRST_USER_SHIFT_X, FIRST_USER_SHIFT_Y = 50, 245

    TO_STICKER_SHIFT_X, TO_STICKER_SHIFT_Y = 395, 120
    STICKER_SHIFT_X, STICKER_SHIFT_Y = 105, 120


class Image:

    # Функция вычисления хэша
    @classmethod
    def calc_image_hash(cls, image) -> str:
        resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
        avg = gray_image.mean()  # Среднее значение пикселя
        ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу

        # Рассчитаем хэш
        _hash = ""
        for x in range(8):
            for y in range(8):
                val = threshold_image[x, y]
                if val == 255:
                    _hash = _hash + "1"
                else:
                    _hash = _hash + "0"

        return _hash

    @staticmethod
    def compare_image_hash(hash1, hash2) -> int:
        l = len(hash1)
        i = 0
        count = 0
        while i < l:
            if hash1[i] != hash2[i]:
                count = count + 1
            i = i + 1
        return count

    @classmethod
    def compare_images(cls, img1, img2) -> int:
        hash_1 = cls.calc_image_hash(img1)
        hash_2 = cls.calc_image_hash(img2)

        return cls.compare_image_hash(hash_1, hash_2)

    @classmethod
    def take_black(cls, src):
        size = src.shape[1], src.shape[0]
        gray_img = cv2.imread("light_gray.png")
        gray_img = cv2.resize(gray_img, size)

        return cv2.add(src, gray_img)


class Worker:
    pos_x, pos_y = 0, 0
    runed = True

    def __init__(self):
        self.first_sticker_compare_num = 0

    def run_config(self):
        root = Tk()

        def set_first_sticker():
            shot = self.scnreenshot_shift(self.pos_x + Consts.TO_STICKER_SHIFT_X,
                                          self.pos_y + Consts.TO_STICKER_SHIFT_Y,
                                          Consts.STICKER_SHIFT_X, Consts.STICKER_SHIFT_Y)
            black = Image.take_black(shot)[95:, :]

            self.first_sticker_compare_num = Image.compare_images(black, cv2.imread("one_sticker.png"))
            print(f"Set: {self.first_sticker_compare_num}")

        bt1 = Button(text="First sticker with 1", command=set_first_sticker)
        bt1.pack()

        bt_start = Button(text="Ok, i'm ready", command=lambda: (root.destroy(), self._run()))
        bt_start.pack()

        root.mainloop()

    def scnreenshot_shift(self, x1, y1, x_shift, y_shift):
        return self.screenshot(x1, y1, x1+x_shift, y1+y_shift)

    @staticmethod
    def screenshot(x1, y1, x2, y2):
        pg.screenshot("test_scr.png")
        shot = cv2.imread("test_scr.png")[y1:y2, x1:x2]

        return shot

    def enter_name(self, last: Iterable, new: str):
        pg.moveTo(self.pos_x + Consts.ENTER_X_SHIFT, self.pos_y + Consts.ENTER_Y_SHIFT)
        pg.click()
        pg.click()

        for _ in last:
            pg.hotkey("right")
            pg.hotkey("backspace")

        pg.write(new)
        pg.hotkey("enter")

    def get_new_name(self, old_name: list, ind: int = 0) -> list:
        if len(old_name) == ind:
            old_name.append(-1)

        old_name[ind] += 1

        if old_name[ind] == len(alphabet):
            old_name[ind] = 0
            return self.get_new_name(old_name, ind+1)

        return old_name

    @staticmethod
    def name_to_str(_name: list) -> str:
        name = ""

        for sym_ind in _name:
            name += alphabet[sym_ind]

        return name

    def stop(self):
        self.runed = False

    def run(self):
        root = Tk()
        root.resizable(False, False)
        root.wm_geometry(Consts.WIN_SIZE)

        kb.add_hotkey("ctrl+s", worker.stop)

        def start():
            self.pos_x, self.pos_y = root.winfo_x(), root.winfo_y()
            root.destroy()
            self.run_config()

        Button(text='start', command=start).pack()
        root.mainloop()

    def delay_loop(self, time_ms: int):
        while self.runed and time_ms > 0:
            time_ms -= 1
            sleep(0.001)

    def _run(self):
        name = [0]
        last_name = ""

        print(self.pos_x, self.pos_y)

        while self.runed:
            self.enter_name(last_name, self.name_to_str(name))
            last_name, name = name, self.get_new_name(name)

            pg.moveTo(self.pos_x + Consts.FIRST_USER_SHIFT_X, self.pos_y + Consts.FIRST_USER_SHIFT_Y)
            self.delay_loop(2000)
            pg.click()
            self.delay_loop(5000)

            shot = self.scnreenshot_shift(self.pos_x+Consts.TO_STICKER_SHIFT_X, self.pos_y+Consts.TO_STICKER_SHIFT_Y,
                                          Consts.STICKER_SHIFT_X, Consts.STICKER_SHIFT_Y)
            black = Image.take_black(shot)[95:, :]

            print("Comparing: ", Image.compare_images(black, cv2.imread("one_sticker.png")) == self.first_sticker_compare_num)

            self.delay_loop(5000)


worker = Worker()
worker.run()