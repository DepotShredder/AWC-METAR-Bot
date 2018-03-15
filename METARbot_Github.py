# Imports required modules
import requests, bs4, re, json, datetime, time, platform, logging
# Checks to see if platform is Darwin-based since caffeine is Mac-only
if platform.system() == "Darwin":
    import caffeine
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Asks the user to input the password and sets a "password" variable equal to the input
print ("Please enter the password for AWC.METAR.bot@gmail.com.")
password = input()

# setupFile = "./METARbot_setup_Github.py".read()
from METARbot_setup_Github import sendHr, sendMin

# Creates variables "caffeineHr" and "caffeineMin" to store usage data
caffeineHr = 0
caffeineMin = 0

# Creates while loop
while True:
    # Creates variable "currentTime" equal to current time
    currentTime = datetime.datetime.now()
    # Configures logging
    logging.basicConfig(filename = "./BotLogs/" + str(currentTime.day) + "." +
    str(currentTime.month) + "." + str(currentTime.year) + "BotLog.txt",
    level = logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(message)s")
    # Prints time for reference
    print(str(currentTime.hour) + ":" + str(currentTime.minute))
    # Logs time
    logging.debug("%(asctime)s")
    # If statement so code only runs at correct time
    if currentTime.hour == sendHr and currentTime.minute == sendMin:
        # Creates variable "emailFile" from contents of emailList_example.txt
        emailFile = open("./emailList_example.txt")
        # Creates variable "emailContent" containing properly formatted dictionary
        emailContent = json.loads(emailFile.read())
        # Creates list "emailList" from the keys of emailContent
        emailList = list(emailContent.keys())
        # Creates list "airportList" from the values of emailContent
        airportList = list(emailContent.values())
        # Creates for loop that runs for every list of airports
        for a in range(len(airportList)):
            # Turns "airportList" into string that works with AviationWeather.gov's URL formatting
            airportList[a] = "+".join(airportList[a])

        # Makes contact with smtp.gmail.com on SSL port 587
        smtpObj = SMTP("smtp.gmail.com", 587)
        smtpObj.ehlo()
        # Starts TLS encryption
        smtpObj.starttls()
        # Creates variable "botEmail" containing bot's email address
        botEmail = "AWC.METAR.bot@gmail.com"
        # Creates while loop
        while True:
            # Try part of try/except statement
            try:
                # Attempts to log in to bot's email account
                smtpObj.login(botEmail,password)
            # Except statement for when an error is thrown
            except:
                print ("Password incorrect. Try again.")
                # Sets "password" equal to input
                password = input()
                # Restarts this while loop to allow multiple login attempts
                continue
            # Breaks out of this while loop
            break

        # Creates for loop that runs for every item in emailContent
        for i in range(len(emailContent)):
            # Creates variable "airport" equal to ith string in airportList
            airport = airportList[i]

            # Sets variable "res" equal to return of AWC link
            res = requests.get("https://aviationweather.gov/metar/data?ids=" +
                           airport + "&format=raw&date=0&hours=0&taf=on")

            # Creates regex to sort for useful data
            wxRegex = re.compile (r"<!-- Data starts here -->(.*)<!-- Data ends here -->", re.DOTALL)
            # Used in previous version
            avWX = bs4.BeautifulSoup(res.text, "html.parser")
            # Narrows down "res" into more useful HTML text
            awcMC = avWX.select ("#awc_main_content")

            # Searches "awcMC" for text matching text described by "wxRegex"
            avMETAR = wxRegex.search(str(awcMC))
            # Changes "avMETAR" from regex object to string
            avMETAR = avMETAR.group()
            # Substitutes <br/> (html linebreak) for \n (Python linebreak)
            avMETAR = re.sub(r"<br/>", "\n", avMETAR)
            # Gets rid of html tags
            avMETAR = bs4.BeautifulSoup(avMETAR, "html.parser")
            # Changes "avMETAR from BeautifulSoup object to string
            avMETAR = avMETAR.text
            # UTF-8 stuff I don't completely understand
            avMETAR = re.sub("\xa0", " ", avMETAR)

            # Prints and logs avMETAR
            print (avMETAR)
            logging.debug(avMETAR)

            # Sets variable "toAdress" equal to ith email
            toAddress = emailList[i]
            # Creates MIMEMultipart-type variable "msg"
            msg = MIMEMultipart()
            # Sets sender to "botEmail"
            msg['From'] = botEmail
            # Sets recipient to "toAddress"
            msg['To'] = toAddress
            # Prints recipient's email
            print("Sent to: " + msg['To'])
            # Logs recipient's email
            logging.debug("Sent to: " + msg["To"])
            # Sets email subject
            msg['Subject'] = "Your Daily Weather"
            # Sets email body to "avMETAR"
            body = avMETAR
            # Unsure of exactly what this does
            msg.attach(MIMEText(body,"plain"))
            # Sends email from "botEmail" to "toAddress" with "msg" formatted as string
            smtpObj.sendmail(botEmail,toAddress,msg.as_string())


        # Closes SMTP connection
        smtpObj.close()
        # Breaks while loop
        break
    # Else statement for when time does not match desired send time
    else:
        # Checks "currentTime" to see if it's safe to set the amount of time to sleep to 1 hour
        if currentTime.hour<(sendHr-1) or currentTime.hour>sendHr:
            # Checks that platform is Darwin-based since caffeine is a Mac command
            if platform.system() == "Darwin":
                print("Running 'caffeine' to prevent the system from sleeping.")
                # Adds 1 to "caffeineMin" every time caffeine runs before time.sleep(3600)
                caffeineHr += 1
                logging.debug("Caffeine has run " + str(caffeineHr) + " times.")
                # Keeps computer awake but allows display to sleep
                caffeine.on(display=False)
            time.sleep(3600)
        # Program sleeps only for 1 minute per loop if time before "currentTime" ≤1hr
        else:
            if platform.system() == "Darwin":
                print("Running 'caffeine' to prevent the system from sleeping.")
                # Adds 1 to "caffeineMin" every time caffeine runs before time.sleep(60)
                caffeineMin += 1
                logging.debug("Caffeine has run " + str(caffeineMin) + " times.")
                # Keeps computer awake but allows display to sleep
                caffeine.on(display=False)
            time.sleep(60)
        # Restarts while loop
        continue
