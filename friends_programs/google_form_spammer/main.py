import mouse
import keyboard
import time
import random


def main():
    list_of_cords_1 = [[(-1307, 397), (-1308, 441)], [(-1305, 574), (-1303, 616), (-1307, 651), (-1305, 692)],
                   [(-1309, 824), (-1310, 864), (-1308, 907)]]
    list_of_cords_2 = [[(-1307, 371), (-1307, 411), (-1309, 448)], [(-1304, 579), (-1308, 623), (-1305, 661)]]
    time.sleep(2)
    for k in range(50):
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

        mouse.move(-1194, 740)
        mouse.click()
        time.sleep(2)

        mouse.move(-765, 55)
        mouse.click()
        keyboard.press_and_release("ctrl+v")
        keyboard.press_and_release("enter")
        time.sleep(2)


if __name__ == "__main__":
    main()
