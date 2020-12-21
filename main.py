from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import traceback,time,datetime,os,argparse,platform,schedule

#checking the platform
if platform.system() == 'Darwin':
    chrome_default_path = os.getcwd()+'/chromedriver'
else:
    chrome_default_path = os.getcwd() + '\chromedriver.exe'

parser = argparse.ArgumentParser(description='PyWhatsapp Guide')
parser.add_argument('--chrome_driver_path', action='store', type=str, default=chrome_default_path,
                    help='chromedriver executable path (MAC and Windows path would be different)')
parser.add_argument('--message', action='store', type=str, default='', help='Enter the msg you want to send')
parser.add_argument('--remove_cache', action='store', type=str, default='False',
                    help='Remove Cache | Scan QR again or Not')
parser.add_argument('--import_contact', action='store', type=str, default='False',
                    help='Import contacts.txt or not (True/False)')
parser.add_argument('--enable_headless', action='store', type=str, default='False',
                    help='Enable Headless Driver (True/False)')
args = parser.parse_args()

if args.remove_cache == 'True':
    os.system('rm -rf User_Data/*')
browser = None
Contact = None
message = None if args.message == '' else args.message
Link = "https://web.whatsapp.com/"
wait = None
choice = None

def input_contacts():
    global Contact
    Contact = []
    while True:
            n = int(input('Enter number of Contacts to add(count): '))
            for i in range(0, n):
                inp = str(input("Enter the saved contact name(text): "))
                inp = '"' + inp + '"'
                Contact.append(inp)
            choi = input("Do you want to add more contacts(y/n): ")
            if choi == "n":
                break
    if len(Contact) != 0:
        print("\nSaved contacts entered list:", Contact)
    input("\nPress ENTER to continue...")

def input_message():
    global message
    print(
        "\nEnter the message and use symbol '~' to end message:\nFor example: Hi, this is a test message~\n\nYour message: ")
    message = []
    done = False

    while not done:
        temp = input()
        if len(temp) != 0 and temp[-1] == "~":
            done = True
            message.append(temp[:-1])
        else:
            message.append(temp)
    message = "\n".join(message)
    print(message)

def whatsapp_login(chrome_path, headless):
    global wait, browser, Link
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=./User_Data')
    if headless == 'True':
        chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    browser.maximize_window()
    print("QR code is Scanned successfully.")

def send_message(target):
    global message, wait, browser
    try:
        x_arg = '//span[contains(@title,' + target + ')]'
        ct = 0
        while ct != 5:
            try:
                group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
                group_title.click()
                break
            except Exception as e:
                print("Retry Send Message Exception", e)
                ct += 1
                time.sleep(3)
        input_box = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for ch in message:
            if ch == "\n":
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(
                    Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
            else:
                input_box.send_keys(ch)
        input_box.send_keys(Keys.ENTER)
        print("Message sent successfully")
        time.sleep(1)
    except NoSuchElementException as e:
        print("send message exception: ", e)
        return

def sender():
    global Contact
    print(Contact)
    for i in Contact:
        try:
            send_message(i)
            print("Message sent to ", i)
        except Exception as e:
            print("Msg to {} send Exception {}".format(i, e))
    time.sleep(5)

def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    if not Contact:
        input_contacts()
    if message == None:
        input_message()

    isSchedule = input('Do you want to schedule your Message(yes/no):')
    if (isSchedule == "yes"):
        jobtime = input('Enter time for sending the message in 24 hour(HH:MM) format - ')

    print("SCAN YOUR QR CODE FOR WHATSAPP WEB")
    whatsapp_login(args.chrome_driver_path, args.enable_headless)

    if isSchedule == "yes":
        schedule.every().day.at(jobtime).do(sender)
    else:
        sender()
        print("Task is Completed Successfully")
    scheduler()
