import spidev
import RPi.GPIO as GPIO

from PIL import ImageFont
from draw.lib_tft24T import TFT24T


class CanvasHelper:

    __FONT = ImageFont.truetype('./fonts/3270 Narrow Nerd Font Complete.ttf', 18)
    __ORIENTATION_DEGREES = 90

    # Raspberry Pi configuration.
    __DC = 24
    __RST = 25
    __LED = 18

    __tft = None

    __MAX_DEVICES = 5

    def __init__(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Create TFT LCD/TOUCH object:
        self.__tft = TFT24T(spidev.SpiDev(), GPIO, landscape=False)

        # Initialize display.
        self.__tft.initLCD(self.__DC, self.__RST, self.__LED)

        self.__tft.clear()

    def draw(self, to_draw):
        self.__draw_internet_speed(to_draw['isp'])
        self.__draw_separator([(75, 320), (75, 170)])
        self.__draw_pihole(to_draw['pihole'])
        self.__draw_separator([(0, 170), (240, 170)])
        self.__draw_qnap(to_draw['qnap'])
        self.__tft.display()

    def __draw_internet_speed(self, isp):
        canvas = self.__tft.draw()
        canvas.textrotated((0, 240), "ISP", self.__ORIENTATION_DEGREES, self.__FONT, "white")
        canvas.textrotated((20, 190), "↓: {}".format(isp['download_speed_mb']), self.__ORIENTATION_DEGREES,
                           self.__FONT, "green")
        canvas.textrotated((37, 200), "↑: {}".format(isp['upload_speed_mb']), self.__ORIENTATION_DEGREES,
                           self.__FONT, "red")
        canvas.textrotated((54, 219), "~: {}".format(isp['ping_ms']), self.__ORIENTATION_DEGREES,
                           self.__FONT, "white")

    def __draw_separator(self, position):
        canvas = self.__tft.draw()
        canvas.line(position, "blue", 1)

    def __draw_pihole(self, pihole):
        canvas = self.__tft.draw()

        canvas.textrotated((78, 232), "PiHole", self.__ORIENTATION_DEGREES, self.__FONT, "white")

        color = self.__get_color_from_text(pihole['status'])

        r = 15
        x = 200
        y = 297

        left_up_point = (x - r, y - r)
        right_down_point = (x + r, y + r)

        two_point_list = [left_up_point, right_down_point]
        degrees_to_fill = 360 * pihole['blocked_ads_percentage'] / 100

        canvas.textrotated((95, 195), "blocked: {0:.0f}".format(pihole['total_blocked']),
                           self.__ORIENTATION_DEGREES, self.__FONT, color)
        canvas.textrotated((115, 188), "total: {0:.0f}".format(pihole['total_queries']),
                           self.__ORIENTATION_DEGREES, self.__FONT, "yellow")

        canvas.pieslice(two_point_list, 0, 360, "yellow")
        canvas.pieslice(two_point_list, 0, degrees_to_fill, color)

        canvas.textrotated((132, 188), "TOP 5:", self.__ORIENTATION_DEGREES,
                           self.__FONT, "blue")

        c = 0
        x_device_pos = 148

        for d in pihole['top_devices']:
            canvas.textrotated((x_device_pos, 180), d, self.__ORIENTATION_DEGREES,
                               self.__FONT, "white")

            if c == self.__MAX_DEVICES:
                break

            c += 1
            x_device_pos += 14

    def __draw_qnap(self, qnap):
        canvas = self.__tft.draw()

        canvas.textrotated((2, 70), "QNAP", self.__ORIENTATION_DEGREES, self.__FONT, "white")

        canvas.textrotated((20, 10), "CPU: {0:.2f}% | {1:.0f}°C".format(qnap['usage']['cpu'],
                                                                        qnap['temperature']['cpu']),
                           self.__ORIENTATION_DEGREES, self.__FONT, self.__get_color(
                                                                            [
                                                                                qnap['usage']['cpu'], qnap['temperature']['cpu']
                                                                            ]))

        canvas.textrotated((35, 62), "MEM: {0:.2f}%".format(qnap['usage']['memory']),
                           self.__ORIENTATION_DEGREES, self.__FONT, self.__get_color(
                                                                            [
                                                                                qnap['usage']['memory']
                                                                            ]))

        canvas.textrotated((50, 62), "HDD: {0:.2f}%".format(qnap['usage']['hdd']),
                           self.__ORIENTATION_DEGREES, self.__FONT, self.__get_color(
                                                                            [
                                                                                qnap['usage']['hdd']
                                                                            ]))

        canvas.textrotated((65, 55), "{0:.2f}°C".format(qnap['temperature']['hdd1']),
                           self.__ORIENTATION_DEGREES, self.__FONT, self.__get_color(
                                                                            [
                                                                                qnap['temperature']['hdd1']
                                                                            ]))

        canvas.textrotated((80, 55), "{0:.2f}°C".format(qnap['temperature']['hdd2']),
                           self.__ORIENTATION_DEGREES, self.__FONT, self.__get_color(
                                                                            [
                                                                                qnap['temperature']['hdd2']
                                                                            ]))

        canvas.textrotated((100, 105), "Health", self.__ORIENTATION_DEGREES, self.__FONT, "white")

        canvas.textrotated((115, 60), "System: {}".format(qnap['health']['system']),
                           self.__ORIENTATION_DEGREES, self.__FONT, self.__get_color_from_text(qnap['health']['system']))
        canvas.textrotated((130, 80), "HDD1: {}".format(qnap['health']['hdd1']),
                           self.__ORIENTATION_DEGREES, self.__FONT, self.__get_color_from_text(qnap['health']['hdd1']))
        canvas.textrotated((145, 80), "HDD2: {}".format(qnap['health']['hdd2']),
                           self.__ORIENTATION_DEGREES, self.__FONT, self.__get_color_from_text(qnap['health']['hdd2']))

    @staticmethod
    def __get_color(amounts):

        color = "green"

        for amount in amounts:
            if amount > 60:
                color = "red"

        return color

    @staticmethod
    def __get_color_from_text(text):
        text = text.lower().strip()

        if text == 'good' or text == 'ok' or text == 'enabled':
            return "green"

        return "red"
