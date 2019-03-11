from os import listdir
from os.path import isfile, join
import glob, os
from icalendar import Calendar, Event
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
import time

##In this file, we will start compile all holidays from countries
##which currencies are served by BCA.

path = "C:\\Users\\u062318\\Documents\\maket bank holiday\\Remittance"

os.chdir(path)
countryList = glob.glob('./*.ics')
print(countryList)
print("\n")

# Python stores and print in alphabetical order.
# Now time to get the country codes in the list. 3 characters only!
ctyCcyPairs = {}
for codes in countryList:
    codes1 = codes.split('_')
    ccd = codes1[0]
    crd = codes1[1]
    ctyCode = ccd[2:]
    currCode= crd
    print(ctyCode, "\t", currCode)
    ctyCcyPairs[ctyCode] = currCode

print(ctyCcyPairs)

countryCodes = list(ctyCcyPairs.keys())

n = len(countryCodes)
hm = []
cy = 2018 #current year
start = time.time()
for i in range(n):
    sf = countryList[i]
    ccd = countryCodes[i]
    ccy = ctyCcyPairs[ccd]

    s = open(sf, 'rb')
    sc = Calendar.from_ical(s.read())

    for component in sc.walk():
        
         if component.name == "VEVENT":
            sm = component.get('summary')
            hd = component.get('dtstart').dt
            hd1 = component.get('dtend').dt

            if (hd.year != cy):
                hm.append({'DTSTART': hd, 'LOCATION': ccd,
                           'DESCRIPTION': ccy,'SUMMARY': sm, 'DTEND': hd1})

end = time.time()
print("it took:", end-start, "seconds")


hm1 = pd.DataFrame(hm)
hm1 = hm1.sort_values(by='DTSTART')
hm1 = hm1.reset_index(drop=True)

##hm1.to_csv("Remittance_Holidays.csv", encoding='utf-8')

daftarCuti = Calendar()
start = time.time()
for i in range(0, len(hm1)):
    evt = Event()

    evt.add('summary', hm1.iloc[i]['SUMMARY'])
    evt.add('location', hm1.iloc[i]['LOCATION'])
    evt.add('description', hm1.iloc[i]['DESCRIPTION'])
    evt.add('dtstart', hm1.iloc[i]['DTSTART'])
    evt.add('dtend', hm1.iloc[i]['DTEND'])

    daftarCuti.add_component(evt)


##print(daftarCuti, "\t\n")
end = time.time()
print("it took:", end-start, "seconds")

ofn = 'Remittance_HolidayLists.ics'

f = open(ofn, 'wb')
f.write(daftarCuti.to_ical())
f.close()



    
