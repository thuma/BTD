import requests
import json
from urllib import quote as urlencode
from datetime import timedelta
from datetime import datetime

s = requests.Session()
    
def getTimetableByDate(date):
    res = s.get("https://www.nettbuss.se/bokning/valj-avgang?s=0-1391-1394-"+date)
    jsondata = res.content.split('var tbWebClientInitOptions =')[1].split('</script>')[0].strip()
    jsondata = jsondata.split('departureSearchResult')[1].split('"currency"')[0].strip()[:-1]
    jsondata =  '{"data"'+jsondata+'}]}'
    timetable = json.loads(jsondata)
    return timetable['data'][0]

def getPrices(key, type):
        url = 'https://www.nettbuss.se/api/v2/DepartureSearchResult/GetDepartureInformation?tripKey='+urlencode(key)+'&toTrip=true&ticketTypeId='+type+'&editing=&allowOnlyOneBooking=false'
        headers = {'Content-type':'application/json'}
        r = s.get(url, headers=headers)
        tripdetails = json.loads(r.content)
        return tripdetails

def addPrices(timetable):
    for id, trip in enumerate(timetable['trips']):
        key = trip['tripKey']
        timetable['trips'][id]['ecoprice'] = getPrices(key, '1')
        timetable['trips'][id]['premiumprice'] = getPrices(key, '2')
    return timetable

today = datetime.today()

for days in range (0,60):
    thedate = today + timedelta(days=days)
    thedate = thedate.strftime("%Y%m%d")
    timetable = addPrices(getTimetableByDate(thedate))
    print json.dumps(timetable)