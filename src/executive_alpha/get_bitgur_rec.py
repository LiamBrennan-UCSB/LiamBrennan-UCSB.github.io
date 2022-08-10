from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium import webdriver
from time import sleep

import matplotlib.pyplot as plt
import cv2
import numpy as np


def get_rec(site='https://bitgur.com/map/last_hour/all/cap'):

    ## get website ##
    service = ChromeService(executable_path=ChromeDriverManager().install())



    driver = webdriver.Chrome(service=service)
    driver.get("https://bitgur.com/map/last_day/all/cap")
    sleep(1)

    ## take screenshot ##
    driver.get_screenshot_as_file("screenshot.png")
    driver.quit()

    ## load screenshot ##
    im = plt.imread("screenshot.png")
    # plt.imshow(im[222:792,63:792])
    # plt.show()

    src_img = im[222:792,63:792]
    average_color_row = np.average(src_img, axis=0)
    average_color = np.average(average_color_row, axis=0)
    print(average_color)

    # plt.plot([])
    # plt.gca().set_facecolor(average_color)
    # plt.show()

    day_greeness = average_color[1]



    driver = webdriver.Chrome(service=service)
    driver.get('https://bitgur.com/map/last_hour/all/cap')
    sleep(1)

    ## take screenshot ##
    driver.get_screenshot_as_file("screenshot.png")
    driver.quit()

    ## load screenshot ##
    im = plt.imread("screenshot.png")
    # plt.imshow(im[222:792,63:792])
    # plt.show()

    src_img = im[222:792,63:792]
    average_color_row = np.average(src_img, axis=0)
    average_color = np.average(average_color_row, axis=0)
    print(average_color)

    # plt.plot([])
    # plt.gca().set_facecolor(average_color)
    # plt.show()

    greeness = average_color[1]
    redness = average_color[0]

    old_greeness = greeness

    if greeness > redness and day_greeness < greeness:
        print("Market's looking good in last hour! Checking 15 min.")
        driver = webdriver.Chrome(service=service)

        driver.get('https://bitgur.com/map/last_minute15/all/cap')
        sleep(1)

        ## take screenshot ##
        driver.get_screenshot_as_file("screenshot.png")
        driver.quit()

        ## load screenshot ##
        im = plt.imread("screenshot.png")
        # plt.imshow(im[222:792,63:792])
        # plt.show()

        src_img = im[222:792,63:792]
        average_color_row = np.average(src_img, axis=0)
        average_color = np.average(average_color_row, axis=0)
        print(average_color)

        # plt.plot([])
        # plt.gca().set_facecolor(average_color)
        # plt.show()

        greeness = average_color[1]
        redness = average_color[0]

        if greeness > redness*1.2 and greeness > 1.1*old_greeness:
            print("Market's looking good in last 15 min! BUY BUY BUY!")

            return 1
        print("Market looks bad in last 15 min. ")
        return 0

    print("Market looks bad in last hour. ")
    return 0

def main():

    get_rec()

if __name__ == '__main__':
    main()