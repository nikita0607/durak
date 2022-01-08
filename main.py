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

    TO_STICKER_SHIFT_X, TO_STICKER_SHIFT_Y = 790, 207
    STICKER_SHIFT_X, STICKER_SHIFT_Y = 105, 120


class Worker:
    pos_x, pos_y = 0, 0
    runed = True

    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.wm_geometry(Consts.WIN_SIZE)

    def scnreenshot_shift(self, x1, y1, x_shift, y_shift):
        return self.screenshot(x1, y1, x1+x_shift, y1+y_shift)

    def screenshot(self, x1, y1, x2, y2):
        shot = pg.screenshot("test_scr.png")
        shot = cv2.imread("test_scr.png")[Consts.TO_STICKER_SHIFT_Y:Consts.TO_STICKER_SHIFT_Y + Consts.STICKER_SHIFT_Y,
               Consts.TO_STICKER_SHIFT_X:Consts.TO_STICKER_SHIFT_X + Consts.STICKER_SHIFT_X]

        return shot

    def take_black(self, src):
        size = src.shape[1], src.shape[0]
        gray_img = cv2.imread("test2.png")
        gray_img = cv2.resize(gray_img, size)

        img = cv2.add(src, gray_img)[95:, :]

        cv2.imwrite("test.png", img)

        cv2.imshow("test", img)
        cv2.waitKey(0)

        return img

    def enter(self, last: Iterable, new: str):
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

        kb.add_hotkey("ctrl+s", worker.stop)
        Button(text='start', command=self._run).pack()
        self.root.mainloop()

    def _run(self):
        name = [0]
        last_name = ""
        self.pos_x, self.pos_y = self.root.winfo_x(), self.root.winfo_y()
        self.root.destroy()
        print(self.pos_x, self.pos_y)

        while self.runed:
            self.enter(last_name, self.name_to_str(name))
            last_name, name = name, self.get_new_name(name)

            pg.moveTo(self.pos_x + Consts.FIRST_USER_SHIFT_X, self.pos_y + Consts.FIRST_USER_SHIFT_Y)
            sleep(2)
            pg.click()
            sleep(5)

            shot = self.scnreenshot_shift(self.pos_x+Consts.TO_STICKER_SHIFT_X, self.pos_y+Consts.TO_STICKER_SHIFT_Y,
                                          Consts.STICKER_SHIFT_X, Consts.STICKER_SHIFT_Y)
            cv2.imshow("test", self.take_black(shot))
            cv2.waitKey(0)

            sleep(5)


worker = Worker()
worker.run()