import re
import unidecode
text = re.compile('"mtriple": \[.*?\]',re.DOTALL)
property = re.compile('(?<=\|).*?(?=\|)')
subject = re.compile('(?<=").*?(?=\|)')
object = re.compile('(?<=\|)[^\|]*?(?=")')
subjects = []
objects = []
propertylist = []
mnth = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July',
        '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
cntries = {' u s ': ' United States ', ' u k ': ' United Kingdom ', ' u s a ': ' United States ', ' n y ': ' new york ', ' n j ': ' new jersey '}
clubs = {' fc ': ' f c ',' asd ': 'a s d', ' ac ': ' a c ',' us ': ' u s ', ' afc ': ' a f c ', ' cd ': ' c d ', ' as ': ' a s ',' ae ': ' a e ', ' bc ': ' b c ', ' ad ': ' a d '}
unseenProperies = [['mascot','[__predicate__ [__object__ object0] is the mascot of [__subject__ subject0] ]','[__predicate__ [__subject__ subject0] has [__object__ object0] as its mascot]','[__predicate__ [__subject__ subject0\'s] mascot is [__object__ object0] ]'],
['established','[__predicate__ [__subject__ subject0] was established in [__object__ object0] ]','[__predicate__ In [__object__ object0], [__subject__ subject0] was established]'],
['academicStaffSize','[__predicate__ [__subject__ subject0] has [__object__ object0] academic staff]'],
['numberOfMembers','[__predicate__ [__subject__ subject0] has [__object__ object0] members]'],
['numberOfUndergraduateStudents','[__predicate__ [__subject__ subject0] has [__object__ object0] graduate students]'],
['inOfficeWhilePresident','[__predicate__ [__subject__ subject0] was in office at the same time as [__object__ object0] was president]'],
['publisher','[__predicate__ [__subject__ subject0] is the publisher of [__object__ object0] ]'],
['inOfficeWhileMonarch','[__predicate__ [__subject__ subject0] was in office during [__object__ object0\'s] reign]'],
['spouse','[__predicate__ [__subject__ subject0\'s] spouse was [__object__ object0] ]'],
['issnNumber','[__predicate__ [__subject__ subject0] has the ISSN number [__object__ object0] ]'],
['author','[__predicate__ [__subject__ subject0] is the author of [__object__ object0] ]'],
['precededBy','[__predicate__ [__subject__ subject0] was preceded by [__object__ object0] ]'],
['foundingDate','[__predicate__ [__subject__ subject0] was founded on [__object__ object0] ]'],
['type','[__predicate__ [__subject__ subject0] is a [__object__ object0] ]'],
['netIncome','[__predicate__ [__subject__ subject0] has a net income of [__object__ object0] ]'],
['category','[__predicate__ [__subject__ subject0] is categorised as a [__object__ object0] ]'],
['owningOrganisation','[__predicate__ [__subject__ subject0] is owned by [__object__ object0] ]'],
['dean','[__predicate__ The dean of [__subject__ subject0] is [__object__ object0] ]'],
['numberOfStudents','[__predicate__ [__subject__ subject0] has [__object__ object0] students]'],
['latinName','[__predicate__ [__subject__ subject0] has the Latin name [__object__ object0] ]'],
['followedBy','[__predicate__ [__subject__ subject0] was followed by [__object__ object0] ]'],
['industry','[__predicate__ [__subject__ subject0] is in [__object__ object0] industry]'],
['neighboringMunicipality','[__predicate__ [__subject__ subject0\'s] neighbor is [__object__ object0] ]'],
['legislature','[__predicate__ [__object__ object0] is the legislature of [__subject__ subject0] ]'],
['academicDiscipline','[__predicate__ [__subject__ subject0] comes under the academic discipline of [__object__ object0] ]'],
['spokenIn','[__predicate__ [__subject__ subject0] is spoken in [__object__ object0] ]'],
['codenCode','[__predicate__ [__subject__ subject0] has the CODEN code [__object__ object0] ]'],
['party','[__predicate__ [__subject__ subject0] was a member of [__object__ object0] ]'],
['service','[__predicate__ [__subject__ subject0] offers [__object__ object0] service]'],
['numberOfEmployees','[__predicate__ [__subject__ subject0] employs [__object__ object0] people]'],
['dedicatedTo','[__predicate__ [__subject__ subject0] is dedicated to [__object__ object0] ]'],
['material','[__predicate__ [__subject__ subject0] is made of [__object__ object0] ]'],
['hasDeputy','[__predicate__ [__subject__ subject0\'s] deputy is [__object__ object0] ]'],
['isPartOfMilitaryConflict','[__predicate__ [__subject__ subject0] took place during [__object__ object0] ]'],
['inOfficeWhileVicePresident','[__predicate__ While [__subject__ subject0] was in office, [__object__ object0] was Vice-President]'],
['predecessor','[__predicate__ [__object__ object0] was the predecessor of [__subject__ subject0] ]'],
['militaryBranch','[__predicate__ [__subject__ subject0] served in [__object__ object0] ]'],
['hasToItsNorthwest','[__predicate__ [__subject__ subject0] has [__object__ object0] to its northwest]'],
['hasToItsNortheast','[__predicate__ [__subject__ subject0] has [__object__ object0] to its northeast]'],
['hasToItsWest','[__predicate__ [__subject__ subject0] has [__object__ object0] to its west]'],
['hasToItsSoutheast','[__predicate__ [__subject__ subject0] has [__object__ object0] to its southeast]'],
['hasToItsNorth','[__predicate__ [__subject__ subject0] has [__object__ object0] to its north]'],
['hasToItsSouthwest','[__predicate__ [__subject__ subject0] has [__object__ object0] to its southwest]'],
['LCCN_number','[__predicate__ [__subject__ subject0] has the LCCN number of [__object__ object0] ]'],
['residence','[__predicate__ [__subject__ subject0] lives in [__object__ object0] ]'],
['nickname','[__predicate__ [__object__ object0] is the nickname for [__subject__ subject0] ]'],
['activeYearsEndDate','[__predicate__ [__subject__ subject0] retired on [__object__ object0] ]'],
['district','[__predicate__ [__subject__ subject0] is located in [__object__ object0] ]'],
['director','[__predicate__ The director of [__subject__ subject0] is [__object__ object0] ]'],
['inOfficeWhilePrimeMinister','[__predicate__ [__subject__ subject0] was in office under Prime Minister [__object__ object0] ]'],
['mediaType','[__predicate__ [__subject__ subject0] is in the [__object__ object0] form]'],
['series','[__predicate__ [__subject__ subject0] is a character in [__object__ object0] ]'],
['motto','[__predicate__ [__subject__ subject0] has the motto [__object__ object0] ]'],
['campus','[__predicate__ [__subject__ subject0\'s] campus is located at [__object__ object0] ]'],
['numberOfPostgraduateStudents','[__predicate__ [__subject__ subject0] has [__object__ object0] postgraduate students]'],
['river','[__predicate__ [__object__ object0] runs through [__subject__ subject0] ],[__predicate__ [__subject__ subject0] is the home to [__object__ object0] ]'],
['editor','[__predicate__ [__object__ object0] is the editor [__subject__ subject0] ],[__predicate__ [__subject__ subject0] is edited by [__object__ object0] ]'],
['influencedBy','[__predicate__ [__subject__ subject0] was influenced by [__object__ object0] ]'],
['gemstone','[__predicate__ [__object__ object0] is the gemstone of [__subject__ subject0] ]'],
['wasGivenTheTechnicalCampusStatusBy','[__predicate__ [__object__ object0] gave [__subject__ subject0] the status of \"Technical Campus\"]'],
['religion','[__predicate__ [__object__ object0] is the religion of [__subject__ subject0] ]'],
['isbnNumber','[__predicate__ [__subject__ subject0] has the ISBN number of [__object__ object0] ]'],
['oclcNumber','[__predicate__ [__subject__ subject0] has the OCLC number of [__object__ object0] ]'],
['champions','[__predicate__ The champions of [__subject__ subject0] are [__object__ object0] ]'],
['shipDraft','[__predicate__ [__subject__ subject0] has a ship draft of [__object__ object0] ]'],
['municipality','[__predicate__ [__subject__ subject0] is in the municipality of [__object__ object0] ]'],
['municipality','[__predicate__ The rector of [__subject__ subject0] is [__object__ object0] ]'],
['notableWork','[__predicate__ [__object__ object0] is a notable work by [__subject__ subject0] ]'],
['broadcastedBy','[__predicate__ [__subject__ subject0] was broadcasted by [__object__ object0] ]'],
['numberOfPages','[__predicate__ [__subject__ subject0] has [__object__ object0] pages]'],
['profession','[__predicate__ [__subject__ subject0] was [__object__ object0] ]'],
['modelStartYear','[__predicate__ [__subject__ subject0] entered production in [__object__ object0] ]'],
['numberOfLocations','[__predicate__ [__subject__ subject0] has [__object__ object0] locations]'],
['protein','[__predicate__ [__subject__ subject0] has [__object__ object0] of protein]'],
['revenue','[__predicate__ [__subject__ subject0] has a revenue of [__object__ object0] ]'],
['doctoralAdvisor','[__predicate__ [__subject__ subject0\'s] doctoral advisor was [__object__ object0] ]'],
['color','[__predicate__ [__subject__ subject0] uses the color [__object__ object0] ]'],
['trainerAircraft','[__predicate__ [__subject__ subject0] uses [__object__ object0] as a trainer aircraft]'],
['operatingIncome','[__predicate__ [__subject__ subject0] has an operating income of [__object__ object0] ]'],
['officialSchoolColour','[__predicate__ The official school colours of [__subject__ subject0] is [__object__ object0] ]','[__predicate__ The official school colours of [__subject__ subject0] are [__object__ object0] and [__object__ object1] ]','[__predicate__ The official school colours of [__subject__ subject0] are [__object__ object0], [__object__ object1] and [__object__ object2] ]'],
['shipDisplacement','[__predicate__ [__subject__ the ship subject0] weighs [__object__ object0] ]'],
['attackAircraft','[__predicate__ the [__subject__ subject0] employs the [__object__ object0] attack aircraft]'],
['aircraftHelicopter','[__predicate__ the [__subject__ subject0] employs a helicopter named the [__object__ object0] ]'],
['2ndRunwaySurfaceType','[__predicate__ the surface type of the 2nd runway at [__subject__ subject0] is [__object__ object0 airport object1] ]'],
['carbohydrate','[__predicate__ [__object__ object0] of carbohydrate are in [__subject__ subject0] ]'],
['failedLaunches', '[__predicate__ [__subject__ subject0] failed [__object__ object0] launches]'],
['universityTeam','[__predicate__ The university team of [__object__ object0] is [__subject__ subject0] ]'],
['website','[__predicate__ the website for [__subject__ subject0] is [__object__ object0] ]'],
['partsType','[__predicate__ [__subject__ subject0] is in [__object__ object0] ]'],['professionalField','[__predicate__ [__subject__ subject0] works in [__object__ object0] ]'],
['totalLaunches','[__predicate__ [__subject__ subject0] launched [__object__ object0] times]'],
['developer','[__predicate__ [__object__ object0] developed [__subject__ subject0] ]'],
['administrativeArrondissement','[__predicate__ [__subject__ subject0] is in the administrative [__object__ object0] ]'],
['nearestCity','[__predicate__ the nearest city to [__subject__ subject0] is [__object__ object0] ]'],
['influencedBy','[__predicate__ [__subject__ subject0] is influenced by [__object__ object0] ]'],
['gemstone','[__predicate__ the gemstone [__subject__ subject0] is found in [__object__ object0] ]'],
['architecture','[__predicate__ the [__subject__ subject0\'s] architecture style is [__object__ object0] ]'],
['impactFactor','[__predicate__ The impact factor of [__subject__ subject0] is [__object__ object0] ]'],
['militaryRank','[__predicate__ [__subject__ subject0]\'s military rank is [__object__ object0] ]'],
['firstAired','[__predicate__ [__subject__ subject0] first aired on [__object__ object0] ]'],
['serviceStartYear','[__predicate__ [__subject__ subject0] started service in [__object__ object0] ]'],
['numberOfVotesAttained','[__predicate__ [__subject__ subject0] received [__object__ object0] votes]'],
['sportsOffered','[__predicate__ [__subject__ subject0] offers the sport [__object__ object0] ]'],
['sportGoverningBody','[__predicate__ [__subject__ subject0] is governed by [__object__ object0] ]'],
['place','[__predicate__ [__subject__ subject0] took place in [__object__ object0] ]'],
['unit','[__predicate__ The unit of [__subject__ subject0] is [__object__ object0] ]'],
['garrison','[__predicate__ the garrison of [__subject__ subject0] is [__object__ object0] ]'],
['chairmanTitle','[__predicate__ The title of the chairman of [__subject__ subject0] is [__object__ object0] ]'],
['productionEndYear','[__predicate__ production of [__subject__ subject0] ended in [__object__ object0] ]'],
['inOfficeWhileGovernor','[__predicate__ [__subject__ subject0] served in office during the governorship of [__object__ object0] ]'],
['deathYear','[__predicate__ [__subject__ subject0] died in [__object__ object0] ]'],['firstPublicationYear','[__predicate__ [__subject__ subject0] was first published in [__object__ object0] ]'],
['longName','[__predicate__ The full name of the [__subject__ subject0] is [__object__ object0] ]'],
['areaUrban','[__predicate__ The urban area of [__subject__ subject0] is [__object__ object0] square kilometres'],
['chief','[__predicate__ the chief of [__subject__ subject0] is [__object__ object0] ]'],
['literaryGenre','[__predicate__ [__subject__ subject0] is considered [__object__ object0] ]'],
['eissnNumber','[__predicate__ The eissn number of [__subject__ subject0] is [__object__ object0] ]'],
['timeZone','[__predicate__ the [__subject__ subject0] is in [__object__] ]'],
['child','[__predicate__ [__subject__ subject0] is the child of [__object__ object0] ]'],
['numberOfRooms','[__predicate__ there are [__object__ object0] rooms in [__subject__ subject0] ]'],
['outlookRanking','[__predicate__ the outlook ranking of [__subject__ subject0] is [__object__ object0] ]'],
['distributingCompany','[__predicate__ [__subject__ subject0] is distributed by [__object__ object0] ]'],
['frequency','[__predicate__ [__subject__ subject0] is published [__object__ object0] ]'],
['servingSize','[__predicate__ the serving size of [__subject__ subject0] is [__object__ object0] ]'],
['served','[__predicate__ [__subject__ subject0] is served [__object__ object0] ]'],
['patronSaint','[__predicate__ the patron saint of [__subject__ subject0] is [__object__ object0] ]'],
['5thRunwaySurfaceType','[__predicate__ the 5th runway of [__subject__ subject0] is composed of [__object__ object0] ]'],
['libraryofCongressClassification','[__predicate__ [__subject__ subject0] is classified [__object__ object0] by the Library of Congress]'],
['percentageOfAreaWater','[__predicate__ [__object__ object0] of [__subject__ subject0] is covered in water]'],
['populationMetro','[__predicate__ [__object__ object0] people live in the [__subject__ subject0] metro]'],
['artist','[__predicate__ [__object__ object0] made [__subject__ subject0] ]'],
['producer','[__predicate__ [__object__ object0] produced [__subject__ subject0] ]'],
['runtime','[__predicate__ [__subject__] runs for [__object__] minutes]'],
['recordedIn','[__predicate__ [__subject__ subject0] is recorded in [__object__ object0] ]'],
['album','[__predicate__ [__subject__ subject0] is heard on [__object__ object0]'],
['releaseDate','[__predicate__ The release date of [__subject__ subject0] is [__object__ object0] ]'],
['cinematography','[__predicate__ the cinematographer of [__subject__ subject0] is [__object__ object0] ]'],
['writer','[__predicate__ [__object__ object0] wrote [__subject__ subject0] ]'],
['training','[__predicate__ [__subject__ subject0] trained at [__object__ object0] ]'],
['musicComposer','[__predicate__ [__object__ object0] composed the music for [__subject__ subject0] ]'],
['budget','the budget for [__subject__ subject0] is [__object__ object0]'],
['knownFor','[__predicate__ [__subject__ subject0] is know for [__object__ object0] ]'],
['certification','[__predicate__ [__subject__ subject0] is certified by [__object__ object0] ]'],
['musicalArtist','[__predicate__ [__subject__ subject0] is by [__object__ object0] ]'],
['gross','[__predicate__ [__subject__ subject0] grossed [__object__ object0] bucks]'],
['staff','[__predicate__ [__subject__ subject0] employs [__object__ object0] ]'],
['numberOfDoctoralStudents','[__predicate__ there are [__object__ object0] PhD students in [__subject__ subject0] ]'],
['editing','[__predicate__ [__object__ object0] edited [__subject__ subject0] ]'],
['imdbId','[__predicate__ the imdb id of [__subject__ subject0] is [__object__ object0] ]'],
['meaning','[__predicate__ the meaning of [__subject__ subject0] is [__object__ object0] ]'],
['citizenship','[__predicate__ [__subject__ subject0]\'s country of citizenship is [__object__ object0] ]'],
['sisterStation','[__predicate__ [__subject__ subject0] is the sister station to [__object__ object0] ]'],
['areaMetro','The area of metro [__subject__ subject0] is [__object__ object0] ]'],
['cosparId','[the cospar id of [__subject__ subject0] is [__object__ object0] ]'],
['timeshiftChannel','[__predicate__ the time shift channel of [__subject__ subject0] is [__object__ object0] ]'],[
'foundingYear','[__predicate__ the founding year of [__subject__ subject0] is [__object__ object0] ]'],
['musicalBand','[__predicate__ [__subject__ subject0] is by [__object__ object0] ]'],
['format','[__predicate__ [__subject__ subject0] is released in [__object__ object0] form]'],
['gridReference','[__predicate__ the grid reference of [__subject__ subject0] is [__object__ object0] ]'],
['dissolutionYear','[__predicate__ the dissolution year of [__subject__ subject0] is [__object__ object] ]'],
['distributingLabel','[__predicate__ [__subject__ subject0] is distributed by [__object__ object0] ]'],
['iso6391Code','[__predicate__ the iso 6391 code of [__subject__ subject0] is [__object__ object0] ]'],
['formerBandMember','[__predicate__ [__subject__ subject0] is a former member of the band [__object__ object0] ]'],
['extinctionDate','[__predicate__ the extinction date of [__subject__ subject0] is [__object__ object0] ]'],
['viceChancellor','[__predicate__ the vice chancellor of [__subject__ subject0] is [__object__ object0] ]'],
['ceremonialCounty','[__predicate__ the ceremonial country of [__subject__ subject0] is [__object__ object0] ]'],
['populationMetroDensity','[__predicate__ the population density of metro [__subject__ subject0] is [__object__ object0] ]'],
['iso6392Code','[__predicate__ the iso 6392 code of [__subject__ subject0] is [__object__ object0] ]'],
['LCCNnumber','[__predicate__ the lccn number of [__subject__ subject0] is [__object__ object0] ]'],
['office','[__predicate__ [__subject__ subject0] held the office of [__object__ object0] ]'],
['founder','[__predicate__ [__object__ object0] is the founder of [__subject__ subject0] ]'],
['rector','[__predicate__ the rector of [__subject__ subject0] is [__object__ object0] ]'],
['colour','[__predicate__ the colour of [__subject__ subject0] is [__object__ object0] ]'],
['abbreviation','[__predicate__ [__object__ object0] abbreviates [__subject__ subject0] ]'],
['address','[__predicate__ the address of [__subject__ subject0] is [__object__ object0] [__object__ object1] [__object__ object2] [__object__ object3] ]']]
everyprperties = []
def properties(filetext):
    filetext = open(filetext, 'r')
    filetex = re.split('category', filetext.read())
    for line in filetex[1:]:
        if not re.search('size": "1"', line):
            break
        #print(line)
        lex = re.search('text": ".*"', line)
        texts = re.search(text, line)
        if texts:
            #print(texts)
            pro = re.sub(' |"','', re.search(property, texts.group()).group())
            if pro not in sum(propertylist, []):
                propertylist.append([pro])
            obje = re.search(object, texts.group()).group()
            if obje not in sum(objects, []):
                objects.append([obje])
            objec = re.sub('_(\(.*?\))?', ' ', re.sub(r'(?<!.) |\\|",?', '', obje))
            for e, p in enumerate(objects):
                if objects[e][0] == obje:
                    if objec not in objects[e]:
                        objects[e].append(objec)
            subj = re.search(subject, texts.group()).group()
            if subj not in sum(subjects, []):
                subjects.append([subj])
            subjec = re.sub('_(\(.*?\))?', ' ', re.sub(r'(?<!.) |\\|",?', '', subj))
            for e, p in enumerate(subjects):
                if subjects[e][0] == subj:
                    if subjec not in subjects[e]:
                        subjects[e].append(subjec)
            complements = (re.sub(' (?!.)', '', unidecode.unidecode(objec)).lower(), re.sub(' (?!.)', '', unidecode.unidecode(subjec)).lower())
            # print(complements)
            sen = re.sub('(?<=[0-9])st|(?<=[0-9])th|(?<=[0-9])nd|text": "|(?<=[0-9]),(?=[0-9])','',f'[__predicate__ {unidecode.unidecode(lex.group())} ]',count=1, flags=re.IGNORECASE).lower()
            if complements[1] != '':
                sen = re.sub(re.escape(complements[1]).lower(),'[__subject__ subject0 ]',sen,count=1,flags=re.IGNORECASE)
            if complements[0] != '':
                sen = re.sub(re.escape(complements[0]).lower(),'[__object__ object0 ]',sen,count=1,flags=re.IGNORECASE)
            sen = re.sub('\]\.',']',sen)
            # print(lex.group())
            # print(sen)
            if not re.search('subject.*object|object.*subject', sen):
                #print((obje, subj))
                #print(complements)
                #print(sen)
                sen = re.sub(' u s a | u s | u k ', lambda x: cntries.get(x.group()), re.sub('\. |\.|-', ' ', re.sub('\(|\)|"', '', sen)))
                for club in clubs:
                    sen = re.sub(f'{club}',clubs[club],sen)
                oje = re.sub('\. |\.0?|-', ' ', re.sub('\(.*?\)|:| language|/ | $|(regional)? airport','', complements[0]))
                sje = re.sub('\. |\.0?|-', ' ', re.sub('\(.*?\)|:| language|/ | $|(regional)? airport','', complements[1]))
                numsject = re.search('([0-9][0-9][0-9][0-9]) ([0-9][0-9]) ([0-9][0-9])', sje)
                numoject = re.search('([0-9][0-9][0-9][0-9]) ([0-9][0-9]) ([0-9][0-9])', oje)
                if numsject:
                    sje = re.sub(numsject.group(2), lambda x: mnth.get(x.group()), sje)
                    #print(sje)
                    for sub in re.split(' ', sje):
                        sen = re.sub(f' {sub}', 'subject0', sen, count=1, flags=re.IGNORECASE)
                    sen = re.sub(' (?=subject0)','[__subject__ ',sen,count=1)
                    sen = re.sub(f'subject0(?!.*subject0)','subject0 ]',sen)
                if numoject:
                    oje = re.sub(numoject.group(2), lambda x: mnth.get(x.group()), oje)
                    #print(oje)
                    for obj in re.split(' ', oje):
                        sen = re.sub(f' {obj}', 'object0', sen, count=1, flags=re.IGNORECASE)
                    sen = re.sub(' (?=object0)', '[__object__ ', sen,count=1)
                    sen = re.sub(f'object0(?!.*object0)','object0 ]', sen)
                if len(sje) >= len(oje):
                    if not numsject:
                        for e, sub in enumerate(re.split(',| or ', sje)):
                            if sub != '':
                                if len(re.split(',| or', oje)) != 1:
                                    if not re.search(sub,oje):
                                        sen = re.sub(sub, f'[__subject__ subject{e} ]', sen, count=1, flags=re.IGNORECASE)
                                else:
                                    sen = re.sub(sub, f'[__subject__ subject{e} ]', sen, count=1, flags=re.IGNORECASE)
                    if not numoject:
                        for e, obj in enumerate(re.split(',| or ', oje)):
                            if obj != '':
                                sen = re.sub(obj, f'[__object__ object{e} ]', sen, count=1, flags=re.IGNORECASE)
                else:
                    if not numoject:
                        for e, obj in enumerate(re.split(',| or ', oje)):
                            if obj != '':
                                if len(re.split(',| or', sje)) != 1:
                                    if not re.search(obj,sje):
                                        sen = re.sub(obj, f'[__object__ object{e} ]', sen, count=1, flags=re.IGNORECASE)
                                else:
                                    sen = re.sub(obj,f'[__object__ object{e} ]',sen,count=1, flags=re.IGNORECASE)
                    if not numsject:
                        for e, sub in enumerate(re.split(',| or ', sje)):
                            if sub != '':
                                sen = re.sub(sub, f'[__subject__ subject{e} ]', sen, count=1, flags=re.IGNORECASE)
                for i in range(0, 5):
                    sen = re.sub(f'object{i}(?=.*?object{i})', '', sen)
                    sen = re.sub(f'subject{i}(?=.*?subject{i})', '', sen)
                #print(sen)
                #print((oje, sje, sen))
            for e, p in enumerate(propertylist):
                if propertylist[e][0] == pro:
                    if sen not in propertylist[e]:
                        if re.search('subject[0-9]?.*object[0-9]?|object[0-9]?.*subject[0-9]?', sen):
                            propertylist[e].append(sen)
                        else:
                            print(complements)
                            print(unidecode.unidecode(lex.group()))
                            print(sje)
                            print(oje)
                            print(sen)
    filetext.close()

def corpus(file,outfile):
    unseenProperties = []
    seenProperties = []
    outfisle = open(outfile, 'w')
    text = open(file, 'r')
    tex = text.readlines()
    for line in tex:
        #print(line)
        line = re.split('_(?=subject)', re.sub('\n','',line[1:]))
        print(line)
        outpt = ''
        for txt in line[1:]:
            print(txt)
            sect = re.sub('subject__', '', re.search('subject__.*?(?=_)', unidecode.unidecode(txt)).group()).lower()
            sect = re.split(',| or ',re.sub('-', ' ', re.sub('\(.*?\)|:| language|/ ', '',re.sub('_(\(.*?\))?', ' ', re.sub(r'(?<!.) |\\|",?', '', unidecode.unidecode(sect))))))
            oect = re.sub('object|_', '', re.search('__object__.*', unidecode.unidecode(txt)).group()).lower()
            oect = re.split(',| or ',re.sub('-', ' ', re.sub('\(.*?\)|:| language|/ ', '',re.sub('_(\(.*?\))?', ' ', re.sub(r'(?<!.) |\\|",?', '', unidecode.unidecode(oect))))))
            prperty = re.sub('__predicate__| ', '', re.search('__predicate__.*?(?=_)', unidecode.unidecode(txt)).group())
            prperties = 0
            for e,p in enumerate(unseenProperies):
                if prperties == 1:
                    break
                elif unseenProperies[e][0] == prperty:
                    try:
                        sentence = unseenProperies[e][1]
                        for e,oje in enumerate(oect):
                            sentence = re.sub(f'object{e}',f'{oje}',sentence,count=1,flags=re.IGNORECASE)
                        for e,sje in enumerate(sect):
                            sentence = re.sub(f'subject{e}',f'{sje}',sentence,count=1,flags=re.IGNORECASE)
                        sentence = re.sub('\[__object__ object[0-9] \]|\[__subject__ subject[0-9] \]','',sentence)
                        outpt = re.sub(' \'s','\'s',outpt+str(sentence)+' ')
                        print(outpt)
                        prperties += 1
                    except IndexError:
                        print('no string for ' + prperty + ' seen before.')
                        outpt = outpt+f'[__predicate__ [__subject__ {" ".join(sect)} ] {prperty} [__object__ {" ".join(oect)} ] ]'+' '
                        if prperty not in unseenProperties:
                            unseenProperties.append(prperty)
            for e, p in enumerate(propertylist):
                if prperties == 1:
                    break
                elif re.sub(' ', '', propertylist[e][0]) == prperty:
                    if prperty not in seenProperties:
                        seenProperties.append(prperty)
                    try:
                        sentence = propertylist[e][1]
                        for e,oje in enumerate(oect):
                            sentence = re.sub(f'object{e}',oje,sentence,count=1,flags=re.IGNORECASE)
                        for e,sje in enumerate(sect):
                            sentence = re.sub(f'subject{e}',sje,sentence,count=1,flags=re.IGNORECASE)
                        sentence = re.sub('\[__object__ object[0-9] \]|\[__subject__ subject[0-9] \]','',sentence)
                        outpt = re.sub(' \'s','\'s',outpt+sentence+' ')
                        print(outpt)
                        prperties += 1
                    except IndexError:
                        print('no string for '+prperty+' seen before.')
                        outpt = outpt+f'[__predicate__ [__subject__ {" ".join(sect)} ] {prperty} [__object__ {" ".join(oect)} ] ]'+' '
                        if prperty not in unseenProperties:
                            unseenProperties.append(prperty)
            if not re.search(f"'{prperty}'",str(propertylist)) and not re.search(f"'{prperty}'",str(unseenProperies)) and not re.search(f"'{prperty}'",str(unseenProperties)):
                print('no string for '+prperty+' seen before.')
                outpt = outpt+prperty+' '
                unseenProperties.append(prperty)
            if prperty not in everyprperties:
                everyprperties.append(prperty)
        outpt = re.sub(' (?!.)','',re.sub('\"', '', re.sub('  ', ' ', outpt + '\n')))
        print(outpt)
        outfisle.write(outpt)
    outfisle.close()
    text.close()
    #for sle in unseenProperties:
    #    print(sle)
    print('number of unseen properties is '+str(len(unseenProperties)))

properties(
    '/home/symon/PycharmProjects/WEBNLG/webnlg-dataset/train.json')
out = open('trainproperties.txt', 'w')
out.write('------------Properties-------------\n')
for prop in propertylist:
    out.write(str(prop) + '\n')
out.write('------------Objects----------------\n')
for object in objects:
    out.write(str(object) + '\n')
out.write('------------Subjects---------------\n')
for subject in subjects:
    out.write(str(subject) + '\n')
out.close()
corpus('/home/symon/PycharmProjects/WEBNLG/2020_v2_en/train.mr','trainskeleton.txt')
properties(
    '/home/symon/PycharmProjects/WEBNLG/webnlg-dataset/dev.json')
out = open('../traindevproperties.txt', 'w')
out.write('------------Properties-------------\n')
for prop in propertylist:
    out.write(str(prop) + '\n')
out.write('------------Objects----------------\n')
for object in objects:
    out.write(str(object) + '\n')
out.write('------------Subjects---------------\n')
for subject in subjects:
    out.write(str(subject) + '\n')
out.close()
corpus('/home/symon/PycharmProjects/WEBNLG/2020_v2_en/valid.mr','devskeleton.txt')
corpus('/home/symon/PycharmProjects/WEBNLG/2020_v2_en/test.mr','testskeleton.txt')
print(len(everyprperties))
print(len([x for x in [e[0] for e in propertylist] if x in everyprperties]))
print([x for x in everyprperties if x not in [e[0] for e in propertylist]])
print([x for x in [e[0] for e in propertylist] if x not in everyprperties])