#!/bin/python3
from time import sleep
from draw import canvas_helper
from configuration import Config
from summary import internet_speed_summary, qnap_summary, pi_hole_summary

CONTINUE_WORKING = True


def main():

    conf = Config().config

    while CONTINUE_WORKING:
        to_draw = {
            'isp': internet_speed_summary.InternetSpeed(conf).get_speed(),
            'qnap': qnap_summary.QnapSummary(conf).get_stats(),
            'pihole': pi_hole_summary.PiHoleSummary(conf).get_stats()
        }

        canvas = canvas_helper.CanvasHelper()
        canvas.draw(to_draw)
        sleep(1)


if __name__ == '__main__':
    main()
