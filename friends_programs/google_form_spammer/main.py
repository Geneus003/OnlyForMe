import mouse
import keyboard
import time
import random


def main():
    list_of_cords_1 = [[(-1302, 401), (-1309, 441)], [(-1306, 573), (-1304, 614), (-1309, 656), (-1307, 696)],
                       [(-1305, 828), (-1305, 865)]]
    list_of_cords_2 = [[(-1308, 298), (-1302, 337), (-1310, 379), (-1307, 412)], [(-1305, 544), (-1304, 591), (-1305, 629), (-1305, 672), (-1304, 707)]]
    time.sleep(2)

    for k in range(80):
        print(k)
        url = "https://forms.office.com/Pages/ResponsePage.aspx?id=rprGyLoy0UOfWfmMlfsie6C3WuyxEhdAmi7nEg-u1gNUM0pINVI0S1UwME5IS1JMTTlXT0ZaM1hWQS4u"

        for i in list_of_cords_1:
            j = i[random.randint(0, len(i)-1)]
            mouse.move(j[0], j[1])
            mouse.click()
            time.sleep(0.3)

        keyboard.press("page down")
        time.sleep(1)

        for i in list_of_cords_2:
            j = i[random.randint(0, len(i)-1)]
            mouse.move(j[0], j[1])
            mouse.click()
            time.sleep(0.3)

        mouse.move(-1308, 778)
        mouse.click()
        time.sleep(1)

        mouse.move(-765, 55)
        mouse.click()
        keyboard.press_and_release("ctrl+v")
        keyboard.press_and_release("enter")
        time.sleep(2)


if __name__ == "__main__":
    main()
