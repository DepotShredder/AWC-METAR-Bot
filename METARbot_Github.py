import requests, bs4, re, ast, datetime, time, caffeine
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print ("Please enter the password for AWC.METAR.bot@gmail.com.")
password = input()

while True:
    currentTime = datetime.datetime.now()
    print(str(currentTime.hour) + ":" + str(currentTime.minute))
    if currentTime.hour == 12 and currentTime.minute == 0:
        emailFile = open("./emailList_example.txt")
        emailContent = emailFile.read()
        emailContent = ast.literal_eval(emailContent)
        airportList = list(emailContent.values())
        emailList = list(emailContent.keys())
        for a in range(len(airportList)):
                airportList[a] = ", ".join(airportList[a])

        smtpObj = SMTP("smtp.gmail.com", 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        botEmail = "AWC.METAR.bot@gmail.com"
        smtpObj.login(botEmail,password)

        for i in range(len(emailContent)):
            airport = airportList[i]

            res = requests.get("https://aviationweather.gov/metar/data?ids=" +
                           airport + "&format=raw&date=0&hours=0&taf=on")

            wxRegex = re.compile (r"<!-- Data starts here -->(.*)<!-- Data ends here -->", re.DOTALL)
            avWX = bs4.BeautifulSoup(res.text, "html.parser")
            awcMC = avWX.select ("#awc_main_content")

            avMETAR = wxRegex.search(str(awcMC))
            avMETAR = avMETAR.group()
            avMETAR = re.sub(r"<br/>", "\n", avMETAR)
            avMETAR = bs4.BeautifulSoup(avMETAR, "html.parser")
            avMETAR = avMETAR.text

            print (avMETAR)

            toAddress = emailList[i]
            msg = MIMEMultipart()
            msg['From'] = botEmail
            msg['To'] = toAddress
            print("Sent to: " + msg['To'])
            msg['Subject'] = "Your Daily Weather"
            body = avMETAR
            msg.attach(MIMEText(body,"plain"))
            smtpObj.sendmail(botEmail,toAddress,msg.as_string())



        smtpObj.close()
        break
    else:
        if currentTime.hour<11 or currentTime.hour>12:
            print("Running 'caffeine' to prevent the system from sleeping.")
            caffeine.on(display=False)
            time.sleep(3600)
        else:
            print("Running 'caffeine' to prevent the system from sleeping.")
            caffeine.on(display=False)
            time.sleep(60)
        continue
        


