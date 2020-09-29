import re
import unidecode
text = re.compile('"mtriple": \[.*?\]',re.DOTALL)
property = re.compile('(?<=\|).*?(?=\|)')
subject = re.compile('(?<=").*?(?=\|)')
object = re.compile('(?<=\|)[^\|]*?(?=")')
subjects = []
objects = []
propertylist = [['address','[_property the address of [_subject subject0] is [_object object0] [_object object1] [_object object2] [_object object3]]']]
mnth = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July',
        '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
cntries = {' u s ': ' United States ', ' u k ': ' United Kingdom ', ' u s a ': ' United States ', ' n y ': ' new york ', ' n j ': ' new jersey '}
clubs = {' fc ': ' f c ',' asd ': 'a s d', ' ac ': ' a c ',' us ': ' u s ', ' afc ': ' a f c ', ' cd ': ' c d ', ' as ': ' a s ',' ae ': ' a e ', ' bc ': ' b c ', ' ad ': ' a d '}
unseenProperies = [['mascot','[_property [_object object0] is the mascot of [_subject subject0]]','[_property [_subject subject0] has [_object object0] as its mascot]','[_property [_subject subject0\'s] mascot is [_object object0]]'],
['established','[_property [_subject subject0] was established in [_object object0]]','[_property In [_object object0], [_subject subject0] was established]'],
['academicStaffSize','[_property [_subject subject0] has [_object object0] academic staff]'],
['numberOfMembers','[_property [_subject subject0] has [_object object0] members]'],
['numberOfUndergraduateStudents','[_property [_subject subject0] has [_object object0] graduate students]'],
['inOfficeWhilePresident','[_property [_subject subject0] was in office at the same time as [_object object0] was president]'],
['publisher','[_property [_subject subject0] is the publisher of [_object object0]]'],
['inOfficeWhileMonarch','[_property [_subject subject0] was in office during [_object object0\'s] reign]'],
['spouse','[_property [_subject subject0\'s] spouse was [_object object0]]'],
['issnNumber','[_property [_subject subject0] has the ISSN number [_object object0]]'],
['author','[_property [_subject subject0] is the author of [_object object0]]'],
['precededBy','[_property [_subject subject0] was preceded by [_object object0]]'],
['foundingDate','[_property [_subject subject0] was founded on [_object object0]]'],
['type','[_property [_subject subject0] is a [_object object0]]'],
['netIncome','[_property [_subject subject0] has a net income of [_object object0]]'],
['category','[_property [_subject subject0] is categorised as a [_object object0]]'],
['owningOrganisation','[_property [_subject subject0] is owned by [_object object0]]'],
['dean','[_property The dean of [_subject subject0] is [_object object0]]'],
['numberOfStudents','[_property [_subject subject0] has [_object object0] students]'],
['latinName','[_property [_subject subject0] has the Latin name [_object object0]]'],
['followedBy','[_property [_subject subject0] was followed by [_object object0]]'],
['industry','[_property [_subject subject0] is in [_object object0] industry]'],
['neighboringMunicipality','[_property [_subject subject0\'s] neighbor is [_object object0]]'],
['legislature','[_property [_object object0] is the legislature of [_subject subject0]]'],
['academicDiscipline','[_property [_subject subject0] comes under the academic discipline of [_object object0]]'],
['spokenIn','[_property [_subject subject0] is spoken in [_object object0]]'],
['codenCode','[_property [_subject subject0] has the CODEN code [_object object0]]'],
['party','[_property [_subject subject0] was a member of [_object object0]]'],
['service','[_property [_subject subject0] offers [_object object0] service]'],
['numberOfEmployees','[_property [_subject subject0] employs [_object object0] people]'],
['dedicatedTo','[_property [_subject subject0] is dedicated to [_object object0]]'],
['material','[_property [_subject subject0] is made of [_object object0]]'],
['hasDeputy','[_property [_subject subject0\'s] deputy is [_object object0]]'],
['isPartOfMilitaryConflict','[_property [_subject subject0] took place during [_object object0]]'],
['inOfficeWhileVicePresident','[_property While [_subject subject0] was in office, [_object object0] was Vice-President]'],
['predecessor','[_property [_object object0] was the predecessor of [_subject subject0]]'],
['militaryBranch','[_property [_subject subject0] served in [_object object0]]'],
['hasToItsNorthwest','[_property [_subject subject0] has [_object object0] to its northwest]'],
['hasToItsNortheast','[_property [_subject subject0] has [_object object0] to its northeast]'],
['hasToItsWest','[_property [_subject subject0] has [_object object0] to its west]'],
['hasToItsSoutheast','[_property [_subject subject0] has [_object object0] to its southeast]'],
['hasToItsNorth','[_property [_subject subject0] has [_object object0] to its north]'],
['hasToItsSouthwest','[_property [_subject subject0] has [_object object0] to its southwest]'],
['LCCN_number','[_property [_subject subject0] has the LCCN number of [_object object0]]'],
['residence','[_property [_subject subject0] lives in [_object object0]]'],
['nickname','[_property [_object object0] is the nickname for [_subject subject0]]'],
['activeYearsEndDate','[_property [_subject subject0] retired on [_object object0]]'],
['district','[_property [_subject subject0] is located in [_object object0]]'],
['director','[_property The director of [_subject subject0] is [_object object0]]'],
['inOfficeWhilePrimeMinister','[_property [_subject subject0] was in office under Prime Minister [_object object0]]'],
['mediaType','[_property [_subject subject0] is in the [_object object0] form]'],
['series','[_property [_subject subject0] is a character in [_object object0]]'],
['motto','[_property [_subject subject0] has the motto [_object object0]]'],
['campus','[_property [_subject subject0\'s] campus is located at [_object object0]]'],
['numberOfPostgraduateStudents','[_property [_subject subject0] has [_object object0] postgraduate students]'],
['river','[_property [_object object0] runs through [_subject subject0]],[_property [_subject subject0] is the home to [_object object0]]'],
['editor','[_property [_object object0] is the editor [_subject subject0]],[_property [_subject subject0] is edited by [_object object0]]'],
['influencedBy','[_property [_subject subject0] was influenced by [_object object0]]'],
['gemstone','[_property [_object object0] is the gemstone of [_subject subject0]]'],
['wasGivenTheTechnicalCampusStatusBy','[_property [_object object0] gave [_subject subject0] the status of \"Technical Campus\"]'],
['religion','[_property [_object object0] is the religion of [_subject subject0]]'],
['isbnNumber','[_property [_subject subject0] has the ISBN number of [_object object0]]'],
['oclcNumber','[_property [_subject subject0] has the OCLC number of [_object object0]]'],
['champions','[_property The champions of [_subject subject0] are [_object object0]]'],
['shipDraft','[_property [_subject subject0] has a ship draft of [_object object0]]'],
['municipality','[_property [_subject subject0] is in the municipality of [_object object0]]'],
['municipality','[_property The rector of [_subject subject0] is [_object object0]]'],
['notableWork','[_property [_object object0] is a notable work by [_subject subject0]]'],
['broadcastedBy','[_property [_subject subject0] was broadcasted by [_object object0]]'],
['numberOfPages','[_property [_subject subject0] has [_object object0] pages]'],
['profession','[_property [_subject subject0] was [_object object0]]'],
['modelStartYear','[_property [_subject subject0] entered production in [_object object0]]'],
['numberOfLocations','[_property [_subject subject0] has [_object object0] locations]'],
['protein','[_property [_subject subject0] has [_object object0] of protein]'],
['revenue','[_property [_subject subject0] has a revenue of [_object object0]]'],
['doctoralAdvisor','[_property [_subject subject0\'s] doctoral advisor was [_object object0]]'],
['color','[_property [_subject subject0] uses the color [_object object0]]'],
['trainerAircraft','[_property [_subject subject0] uses [_object object0] as a trainer aircraft]'],
['operatingIncome','[_property [_subject subject0] has an operating income of [_object object0]]'],
['officialSchoolColour','[_property The official school colours of [_subject subject0] is [_object object0]]','[_property The official school colours of [_subject subject0] are [_object object0] and [_object object1]]','[_property The official school colours of [_subject subject0] are [_object object0], [_object object1] and [_object object2]]'],['shipDisplacement','[_property [_subject the ship subject0] weighs [_object object0]]'],['attackAircraft','[_property the [_subject subject0] employs the [_object object0] attack aircraft]'],
                    ['aircraftHelicopter','[_property the [_subject subject0] employs a helicopter named the [_object object0]]'],['2ndRunwaySurfaceType','[_property the surface type of the 2nd runway at [_subject subject0] is [_object object0 airport object1]]'],
                    ['carbohydrate','[_property [_object object0] of carbohydrate are in [_subject subject0]]'],['failedLaunches', '[_property [_subject subject0] failed [_object object0] launches]'],['universityTeam','[_property The university team of [_object object0] is [_subject subject0]]'],
                    ['website','[_property the website for [_subject subject0] is [_object object0]]'],['partsType','[_property [_subject subject0] is in [_object object0]]'],['professionalField','[_property [_subject subject0] works in [_object object0]]'],['totalLaunches','[_property [_subject subject0] launched [_object object0] times]'],
                    ['developer','[_property [_object object0] developed [_subject subject0]]'],['administrativeArrondissement','[_property [_subject subject0] is in the administrative [_object object0]]'],['nearestCity','[_property the nearest city to [_subject subject0] is [_object object0]]'],['influencedBy','[_property [_subject subject0] is influenced by [_object object0]]'],['gemstone','[_property the gemstone [_subject subject0] is found in [_object object0]]'],['architecture','[_property the [_subject subject0\'s] architecture style is [_object object0]]'],['impactFactor','[_property The impact factor of [_subject subject0] is [_object object0]]'],['militaryRank','[_property [_subject subject0]\'s military rank is [_object object0]]'],['firstAired','[_property [_subject subject0] first aired on [_object object0]]'],['serviceStartYear','[_property [_subject subject0] started service in [_object object0]]'],['numberOfVotesAttained','[_property [_subject subject0] received [_object object0] votes]'],['sportsOffered','[_property [_subject subject0] offers the sport [_object object0]]'],['sportGoverningBody','[_property [_subject subject0] is governed by [_object object0]]'],['place','[_property [_subject subject0] took place in [_object object0]]'],['unit','[_property The unit of [_subject subject0] is [_object object0]]'],['garrison','[_property the garrison of [_subject subject0] is [_object object0]]'],['chairmanTitle','[_property The title of the chairman of [_subject subject0] is [_object object0]]'],['productionEndYear','[_property production of [_subject subject0] ended in [_object object0]]'],['inOfficeWhileGovernor','[_property [_subject subject0] served in office during the governorship of [_object object0]]'],['deathYear','[_property [_subject subject0] died in [_object object0]]'],['firstPublicationYear','[_property [_subject subject0] was first published in [_object object0]]'],['longName','[_property The full name of the [_subject subject0] is [_object object0]]'],['areaUrban','[_property The urban area of [_subject subject0] is [_object object0] square kilometres'],['chief','[_property the chief of [_subject subject0] is [_object object0]]'],['literaryGenre','[_property [_subject subject0] is considered [_object object0]]'],['eissnNumber','[_property The eissn number of [_subject subject0] is [_object object0]]'],['timeZone','[_property the [_subject subject0] is in [_object]]'],['child','[_property [_subject subject0] is the child of [_object object0]]'],['numberOfRooms','[_property there are [_object object0] rooms in [_subject subject0]]'],['outlookRanking','[_property the outlook ranking of [_subject subject0] is [_object object0]]'], ['distributingCompany','[_property [_subject subject0] is distributed by [_object object0]]'],['frequency','[_property [_subject subject0] is published [_object object0]]'], ['servingSize','[_property the serving size of [_subject subject0] is [_object object0]]'],['served','[_property [_subject subject0] is served [_object object0]]'],['patronSaint','[_property the patron saint of [_subject subject0] is [_object object0]]'],['5thRunwaySurfaceType','[_property the 5th runway of [_subject subject0] is composed of [_object object0]]'],['libraryofCongressClassification','[_property [_subject subject0] is classified [_object object0] by the Library of Congress]'],['percentageOfAreaWater','[_property [_object object0] of [_subject subject0] is covered in water]'],['populationMetro','[_property [_object object0] people live in the [_subject subject0] metro]'],['artist','[_property [_object object0] made [_subject subject0]]'],['producer','[_property [_object object0] produced [_subject subject0]]'],['runtime','[_property [_subject] runs for [_object] minutes]'],['recordedIn','[_property [_subject subject0] is recorded in [_object object0]]'],['album','[_property [_subject subject0] is heard on [_object object0]'],['releaseDate','[_property The release date of [_subject subject0] is [_object object0]]'],['cinematography','[_property the cinematographer of [_subject subject0] is [_object object0]]'],['writer','[_property [_object object0] wrote [_subject subject0]]'],['training','[_property [_subject subject0] trained at [_object object0]]'],['musicComposer','[_property [_object object0] composed the music for [_subject subject0]]'],['budget','the budget for [_subject subject0] is [_object object0]'],['knownFor','[_property [_subject subject0] is know for [_object object0]]'],['certification','[_property [_subject subject0] is certified by [_object object0]]'],['musicalArtist','[_property [_subject subject0] is by [_object object0]]'],['gross','[_property [_subject subject0] grossed [_object object0] bucks]'],['staff','[_property [_subject subject0] employs [_object object0]]'],['numberOfDoctoralStudents','[_property there are [_object object0] PhD students in [_subject subject0]]'],['editing','[_property [_object object0] edited [_subject subject0]]'],['imdbId','[_property the imdb id of [_subject subject0] is [_object object0]]'],['meaning','[_property the meaning of [_subject subject0] is [_object object0]]'],['citizenship','[_property [_subject subject0]\'s country of citizenship is [_object object0]]'],['sisterStation','[_property [_subject subject0] is the sister station to [_object object0]]'],['areaMetro','The area of metro [_subject subject0] is [_object object0]]'],['cosparId','[the cospar id of [_subject subject0] is [_object object0]]'],['timeshiftChannel','[_property the time shift channel of [_subject subject0] is [_object object0]]'],['foundingYear','[_property the founding year of [_subject subject0] is [_object object0]]'],['musicalBand','[_property [_subject subject0] is by [_object object0]]'],['format','[_property [_subject subject0] is released in [_object object0] form]'], ['gridReference','[_property the grid reference of [_subject subject0] is [_object object0]]'],['dissolutionYear','[_property the dissolution year of [_subject subject0] is [_object object]]'],['distributingLabel','[_property [_subject subject0] is distributed by [_object object0]]'],['iso6391Code','[_property the iso 6391 code of [_subject subject0] is [_object object0]]'],['formerBandMember','[_property [_subject subject0] is a former member of the band [_object object0]]'],['extinctionDate','[_property the extinction date of [_subject subject0] is [_object object0]]'],['viceChancellor','[_property the vice chancellor of [_subject subject0] is [_object object0]]'],['ceremonialCounty','[_property the ceremonial country of [_subject subject0] is [_object object0]]'],['populationMetroDensity','[_property the population density of metro [_subject subject0] is [_object object0]]'],['iso6392Code','[_property the iso 6392 code of [_subject subject0] is [_object object0]]']]
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
            sen = re.sub('(?<=[0-9])st|(?<=[0-9])th|(?<=[0-9])nd|text": "|(?<=[0-9]),(?=[0-9])','',f'[_property {unidecode.unidecode(lex.group())}]',count=1, flags=re.IGNORECASE).lower()
            if complements[1] != '':
                sen = re.sub(re.escape(complements[1]).lower(),'[_subject subject0]',sen,count=1,flags=re.IGNORECASE)
            if complements[0] != '':
                sen = re.sub(re.escape(complements[0]).lower(),'[_object object0]',sen,count=1,flags=re.IGNORECASE)
            # print(lex.group())
            # print(sen)
            if not re.search('subject.*object|object.*subject', sen):
                print((obje, subj))
                print(complements)
                print(sen)
                sen = re.sub(' u s a | u s | u k ', lambda x: cntries.get(x.group()), re.sub('\. |\.|-', ' ', re.sub('\(|\)|"', '', sen)))
                for club in clubs:
                    sen = re.sub(f'{club}',clubs[club],sen)
                oje = re.sub('\. |\.0?|-', ' ', re.sub('\(.*?\)|:| language|/ | $|(regional)? airport','', complements[0]))
                sje = re.sub('\. |\.0?|-', ' ', re.sub('\(.*?\)|:| language|/ | $|(regional)? airport','', complements[1]))
                numsject = re.search('([0-9][0-9][0-9][0-9]) ([0-9][0-9]) ([0-9][0-9])', sje)
                numoject = re.search('([0-9][0-9][0-9][0-9]) ([0-9][0-9]) ([0-9][0-9])', oje)
                if numsject:
                    sje = re.sub(numsject.group(2), lambda x: mnth.get(x.group()), sje)
                    print(sje)
                    for sub in re.split(' ', sje):
                        sen = re.sub(f' {sub}', 'subject0', sen, count=1, flags=re.IGNORECASE)
                    sen = re.sub(' (?=subject0)','[_subject ',sen,count=1)
                    sen = re.sub(f'subject0(?!.*subject0)','subject0]',sen)
                if numoject:
                    oje = re.sub(numoject.group(2), lambda x: mnth.get(x.group()), oje)
                    print(oje)
                    for obj in re.split(' ', oje):
                        sen = re.sub(f' {obj}', 'object0', sen, count=1, flags=re.IGNORECASE)
                    sen = re.sub(' (?=object0)', '[_object ', sen,count=1)
                    sen = re.sub(f'object0(?!.*object0)','object0]', sen)
                if len(sje) >= len(oje):
                    if not numsject:
                        for e, sub in enumerate(re.split(',| or ', sje)):
                            if sub != '':
                                if len(re.split(',| or', oje)) != 1:
                                    if not re.search(sub,oje):
                                        sen = re.sub(sub, f'[_subject subject{e}]', sen, count=1, flags=re.IGNORECASE)
                                else:
                                    sen = re.sub(sub, f'[_subject subject{e}]', sen, count=1, flags=re.IGNORECASE)
                    if not numoject:
                        for e, obj in enumerate(re.split(',| or ', oje)):
                            if obj != '':
                                sen = re.sub(obj, f'[_object object{e}]', sen, count=1, flags=re.IGNORECASE)
                else:
                    if not numoject:
                        for e, obj in enumerate(re.split(',| or ', oje)):
                            if obj != '':
                                if len(re.split(',| or', sje)) != 1:
                                    if not re.search(obj,sje):
                                        sen = re.sub(obj, f'[_object object{e}]', sen, count=1, flags=re.IGNORECASE)
                                else:
                                    sen = re.sub(obj,f'[_object object{e}]',sen,count=1, flags=re.IGNORECASE)
                    if not numsject:
                        for e, sub in enumerate(re.split(',| or ', sje)):
                            if sub != '':
                                sen = re.sub(sub, f'[_subject subject{e}]', sen, count=1, flags=re.IGNORECASE)
                for i in range(0, 5):
                    sen = re.sub(f'object{i}(?=.*?object{i})', '', sen)
                    sen = re.sub(f'subject{i}(?=.*?subject{i})', '', sen)
                print(sen)
                print((oje, sje, sen))
            for e, p in enumerate(propertylist):
                if propertylist[e][0] == pro:
                    if sen not in propertylist[e]:
                        if re.search('subject[0-9]?.*object[0-9]?|object[0-9]?.*subject[0-9]?', sen):
                            propertylist[e].append(sen)
    filetext.close()

def corpus(file,outfile):
    unseenProperties = []
    seenProperties = []
    outfisle = open(outfile, 'w')
    text = open(file, 'r')
    tex = text.readlines()
    for line in tex:
        line = re.split('__(?=subject)', re.sub('\n','',line[1:]))
        outpt = ''
        for txt in line:
            sect = re.sub('subject__', '', re.search('subject__.*?(?=_)', unidecode.unidecode(txt)).group()).lower()
            sect = re.split(',| or ',re.sub('\. |\.|-', ' ', re.sub('\(.*?\)|:| language|/ ', '',re.sub('_(\(.*?\))?', ' ', re.sub(r'(?<!.) |\\|",?', '', unidecode.unidecode(sect))))))
            oect = re.sub('__object__', '', re.search('__object__.*', unidecode.unidecode(txt)).group()).lower()
            oect = re.split(',| or ',re.sub('\. |\.|-', ' ', re.sub('\(.*?\)|:| language|/ ', '',re.sub('_(\(.*?\))?', ' ', re.sub(r'(?<!.) |\\|",?', '', unidecode.unidecode(oect))))))
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
                        sentence = re.sub('object[0-9]|subject[0-9]','',sentence)
                        outpt = re.sub(' \'s','\'s',outpt+str(sentence)+'. ')
                        prperties += 1
                    except IndexError:
                        #print('no string for ' + prperty + ' seen before.')
                        outpt = outpt+prperty+'. '
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
                        sentence = re.sub('object[0-9]|subject[0-9]','',sentence)
                        outpt = re.sub(' \'s','\'s',outpt+sentence+'. ')
                        prperties += 1
                    except IndexError:
                        #print('no string for '+prperty+' seen before.')
                        outpt = outpt+prperty+'. '
                        if prperty not in unseenProperties:
                            unseenProperties.append(prperty)
            if not re.search(prperty,str(propertylist)) and not re.search(prperty,str(unseenProperies)) and not re.search(prperty,str(unseenProperties)):
                #print('no string for ' + prperty + ' seen before.')
                outpt = outpt+prperty+'. '
                unseenProperties.append(prperty)
            if prperty not in everyprperties:
                everyprperties.append(prperty)
        outpt = re.sub(' \.','.',re.sub('\.\.','.',re.sub('  ',' ',outpt+'\n')))
        outfisle.write(str(outpt))
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
out = open('traindevproperties.txt', 'w')
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