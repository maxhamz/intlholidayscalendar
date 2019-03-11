from os import listdir
from os.path import isfile, join
import glob, os, time, itertools
from icalendar import Calendar, Event
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd

##In this file, we will start compile all holidays from countries
##which currencies are served by BCA.

#path = "C:\\Users\\u062318\\Documents\\maket bank holiday\\Remittance"
path = "/storage/emulated/0/workspace/maketholiday/maketholiday/Internationals/"

##path = '/private/var/mobile/Containers/Shared/AppGroup/FBE9C59E-58D5-4AAF-89D6-421CC9E49E02/Pythonista3/Documents/Remittance/'

os.chdir(path)
countryList = glob.glob('./*.ics') # grab all filenames of *.ics files in the specified working directory.
cy = 2018 #current year
daftarCuti = Calendar()
listHolidays = []
ctyCcyPairs = {}

##countryList contains all *.ics files with country names and currency codes. pairCountryCurrency() function will extract the country names
##and the corresponding currency in that country, and then, pair the country names and currency used into a dictionary.
def pairCountryCurrency():
    
    for codes in countryList:
        codes1 = codes.split('_')
        ccd = codes1[0]
        crd = codes1[1]
        ctyCode = ccd[2:]
        currCode= crd
##        print(ctyCode, "\t", currCode)
        ctyCcyPairs[ctyCode] = currCode



##decomposeCalender() will first extract ALL dictionary keys (aka the country names) from the dictionary returned by the pairCountryCurrency() function.
##Then, an iterative will simultaenously walk thru each filename, country name and currency code, calling the walkThruCalendar() function to decompose the
##important events/holidays saved from Google Calendar, and put those decomposed events into a list of holidays/events, for our compilation later on.
def decomposeCalendar():
	
	for sf, [ccd, ccy] in zip(countryList, ctyCcyPairs.items()):
		s = open(sf, 'rb')
		sc = Calendar.from_ical(s.read())
		for component in sc.walk():
			if component.name == "VEVENT" :
				sm = component.get('summary')
				hd = component.get('dtstart').dt
				hd1 = component.get('dtend').dt
				
				if (hd.year != cy):
					listHolidays.append({'DTSTART': hd, 'LOCATION': ccd,
        			'DESCRIPTION': ccy,'SUMMARY': sm, 'DTEND': hd1})


##sortEvents() will take the event list input (wtc), convert them into
##dataframe, sort them by date, and reset the indexing. That way,
##events aka holidays are now in chronological order.
def sortEvents():
    dfHolidays = pd.DataFrame(listHolidays)
    dfHolidays.sort_values(by='DTSTART')
    dfHolidays.reset_index(drop=True)
    print(dfHolidays, '\t', '\n')
    print(len(dfHolidays))
    
    return dfHolidays




# This function will create a consolidated .ics calendar
# with holidays that are recorded in the list that we created.
# Holidays are recorded as events, with important components of:
# summary, start date, end date, and descriptions.
def put2Calendar():
	dfh = sortEvents()
	for i in range(0, len(dfh)):
		evt = Event()
		evt.add('summary', dfh.iloc[i]['SUMMARY'])
		evt.add('location', dfh.iloc[i]['LOCATION'])
		evt.add('description', dfh.iloc[i]['DESCRIPTION'])
		evt.add('dtstart', dfh.iloc[i]['DTSTART'])
		evt.add('dtend', dfh.iloc[i]['DTEND'])
		daftarCuti.add_component(evt)



# save the calendar as *.ics file in the specified directory
def xport2Directory(ofn):
    ofn1=ofn+".ics"
    f = open(ofn1, 'wb')
    f.write(daftarCuti.to_ical())
    f.close()



def main():
	pairCountryCurrency()
	decomposeCalendar()
	put2Calendar()
	xport2Directory("IntlHolidays20192020")
	


main()


