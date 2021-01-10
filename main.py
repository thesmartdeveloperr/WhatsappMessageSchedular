from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time,os,argparse,platform,schedule

if platform.system() == 'Darwin':
    chrome_default_path = os.getcwd() +'/chromedriver'
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
            n = int(input('Enter number of people to send messages to: '))
            for i in range(0, n):
                inp = str(input("Enter the contact name(the same text as saved on your phone): "))
                inp = '"' + inp + '"'
                Contact.append(inp)
            choi = input("Do you want to add more contacts to send to?(y/n): ")
            if choi == "n" or choi=="no":
                break
    if len(Contact) != 0:
        print("\nYou have selected the contacts: ", Contact)
    input("\nPlease press ENTER to continue...")

def input_message():
    global message
    global frequency
    print(
        "\nEnter the message you want to send or schedule to send later and use symbol '~' to end your message:\nFor example: Hi, this is a test message~\n\nYour message: ")
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
    frequency=int(input('How many times do you want to send this message?[enter a number]'))
    print('YOUR MESSAGE IS:')
    print('__________________________________________________________')
    print(message)
    print('__________________________________________________________')
    print('AND THE NUMBER OF TIMES YOU ARE SENDING THIS MESSAGE IS:',frequency)

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
        # time.sleep(1)
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
    # time.sleep(5)

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
        for i in range(frequency):
            schedule.every().day.at(jobtime).do(sender)
    else:
        for i in range(frequency):
            sender()
        print("Task is Completed Successfully")
    scheduler()
    
    # end of project :)
