import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import tkinter
from pynput.keyboard import Key, Listener
from random import randrange
from functools import partial
import json

PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
# this is only for disabling the 'automation testing baner
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(executable_path=PATH, options=options)

# window app initialization
root = tkinter.Tk()

#initailizing config file
with open('proner_cfg.json') as f:
    data = json.load(f)

# globals
globalpref = ""
loggedin = False
ff = 1
movielist = []

def on_release(key):
    if key == Key.space:
        main(globalpref)
    elif key == Key.esc:
        driver.quit()
    elif key == Key.ctrl_l:
        fastforward()
    elif key == Key.shift_l:
        rate("down")
        main(globalpref)


def on_press(key):
    pass


def rate(r):
    try:
        if r == "up":
            thumb = driver.find_element_by_class_name("js-voteUp")
        elif r == "down":
            thumb = driver.find_element_by_class_name("js-voteDown")
        else:
            pass
        thumb.click()
    except:
        fullscreen()
        rate(r)


def fastforward():
    global ff
    if ff == 10:
        ff = 1
        rate("up")
        main(globalpref)
    actions = ActionChains(driver)
    actions.send_keys(str(ff))
    actions.perform()
    ff = ff + 1


def selectrandom(link):
    global movielist
    driver.get(link)
    x = randrange(2, 22)
    if globalpref == "1":
        video = driver.find_element_by_css_selector("div#recommendations>div>div:nth-of-type(3)>ul>li:nth-of-type(" + str(x) + ")>div>div>a")
    try:
        video.click()
    except:
        driver.execute_script("window.scrollTo(0, 1080)")
        video.click()
    title = driver.execute_script("return document.title;")
    if title in movielist:
        print('this movie has been watched already, switching to a new one')
        main(globalpref)
    movielist.append(title)


def selectnext():
    x = randrange(1,36)
    video = driver.find_element_by_css_selector("#relatedVideosCenter")
    video.click()


def fullscreen():
    video = driver.find_element_by_css_selector("#player > video-element")
    time.sleep(0.1)
    actionChains = ActionChains(driver)
    actionChains.double_click(video).perform()


def adbuster():
    # there is a better way to handle ads (e.g. using chrome adblock extension) but I wanted to test out selenium itself
    while True:
        try:
            chwd = driver.window_handles
            if len(chwd) == 1:
                break
            #this for loop should dismiss any ad notications but it is not working properly yet
            # for c in chwd:
            #     try:
            #         driver.switch_to.window(c)
            #         driver.switch_to.alert().dismiss()
            #     except:
            #         print('no alert detected')
            driver.switch_to.window(chwd[-1])
            print('closing'+chwd[-1])
            driver.close()
        finally:
            break

    driver.switch_to.window(chwd[0])


def pussywagon():

    root.title("Pussy Wagon")
    root.geometry("300x300+1500+700")

    l1 = tkinter.Label(root, text="Pussy Wagon")
    l1.pack()

    b1 = tkinter.Button(root, text="Recommended", command=partial(main, "1"))
    b1.pack()

    b2 = tkinter.Button(root, text="Recommended with login", command=partial(main, "2"))
    b2.pack()

    l2 = tkinter.Label(root, text="HOTKEYS\nspacebar to play next random \nleft ctrl to fast forward 10% \nleft shift to dislike and play next random \nfast forward to 100% to like video and play next random \nesc to ragequit when someone walks in")
    l2.pack(side="bottom")

    root.mainloop()


def preferences():
    global globalpref
    if globalpref == "1":
        if loggedin:
            x = randrange(1, 39)
        else:
            x = randrange(1, 4)
        link = data["recommendedpage"] + str(x)
    elif globalpref == "2":
        login()
        globalpref = "1"
        x = randrange(1, 39)
        link = data["recommendedpage"] + str(x)
    else:
        link = "eror kurde"
    return link


def login():
    driver.get(data["loginpage"])
    try:
        driver.find_element_by_css_selector("#username").send_keys(data["login"])
        driver.find_element_by_css_selector("#password").send_keys(data["pass"])
        time.sleep(0.2)
        driver.find_element_by_css_selector("#submit").click()
        time.sleep(1)
        global loggedin
        loggedin = True
    except:
        print("cannot log in... retrying")
        login()


def automater():
    time.sleep(2)
    main(globalpref)


def exceptionhandling(e):
    print(e)
    if driver.execute_script("return document.title;") == "Strona nie istnieje":
        print("eror 'Strona nie istnieje', Resolving...")
        main(globalpref)
    elif "Unable to locate element" in e:
        print("Unable to locate element")
        print('Resolving...')
        main(globalpref)
    else:
        print("eror maintenance---------------------------------------------------")
        print(e)


def main(pref):

    global globalpref
    globalpref = pref
    global ff
    ff = 1

    try:
        selectrandom(preferences())
        fullscreen()
        adbuster()
        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        exceptionhandling(e)


pussywagon()
