import urllib.request
import os
import re
import random
import pandas as pd

# Grab the csv file with all urls required for picture downloads
chunksize = 10**6
TextFileReader = pd.read_csv('image_urls.csv', sep=',', chunksize=chunksize, iterator=True,low_memory=False,header=None)
image_urls = pd.concat(TextFileReader, ignore_index=True)

# Specify the category names outlined in project specification
names={1:'bad',2:'baumarkt',3:'buero',4:'dekoration',5:'kueche-und-esszimmer',6:'flur-und-diele',7:'garten',
       8:'heimtextilien',9:'kinderzimmer',10:'lampen',11:'schlafzimmer',12:'wohnzimmer',13:'armaturen',
       14:'bad-accessoires',15:'badewannen-und-whirlpools',16:'badgarnituren',17:'badlampen',18:'badmoebel',
       19:'duschen',20:'handtuecher',21:'sauna-und-zubehoer',22:'spiegel',23:'waschbecken',24:'wcs',25:'bad-und-sanitaer',
       26:'bodenbelaege',27:'briefkaesten',28:'camping-und-zubehoer',29:'elektroinstallation',30:'garagen-und-carports',
       31:'heizung-und-klima',32:'kamine-und-oefen',33:'leitern-und-treppen',34:'malern-und-tapezieren',
       35:'modernisieren-und-bauen',36:'wand-und-decke',37:'werkbank',38:'werkzeug',39:'buerobedarf',40:'buerolampen',
       41:'bueromoebelserien',42:'papierkoerbe',43:'raumklima',44:'raumteiler',45:'regale',46:'schraenke',47:'stuehle',
       48:'tafeln-und-boards',49:'tische',50:'accessoires',51:'aufbewahrung',52:'bilder-und-rahmen',53:'dekopflanzen',
       54:'figuren-und-skulpturen',55:'kerzen-und-kerzenstaender',56:'spiegel',57:'textilien',58:'uhren',59:'vasen',
       60:'wandtattoos',61:'zimmerbrunnen',62:'aufbewahrung',63:'bar-moebel',64:'besteck-und-geschirr',65:'elektrogeraete',
       66:'essgruppen',67:'gardinen-und-vorhaenge',68:'kochen-backen',69:'jalousien-und-rollos',70:'kaffee-und-tee',
       71:'kuechen',72:'kuechengeraete',73:'kuechenregale',74:'kuechentextilien',75:'schraenke',76:'servierwagen',
       77:'sitzbaenke',78:'spuelen',79:'stuehle-und-hocker',80:'tische',81:'zubehoer',82:'fussmatten',83:'garderoben',
       84:'haushaltsgeraete',85:'laeufer',86:'lampen',87:'mehrzweckschraenke',88:'regale',89:'schirmstaender',
       90:'schluesselkaesten',91:'schuhschraenke',92:'spiegel',93:'telefontische',94:'aussenlampen',95:'balkon',
       96:'bodenbelaege-garten',97:'brunnen',98:'dekoration',99:'feuer-und-heizstrahler',100:'gartengeraete',
       101:'gartenhaeuser',102:'gartenmoebel',103:'geraetehaeuser',104:'gewaechshaeuser',105:'grill-und-zubehoer',
       106:'haengematten',107:'pavillons',108:'pflanzen',109:'rasenmaeher-und-rasentraktoren',
       110:'sonnenschirme-und-markisen',111:'strandkoerbe',112:'swimmingpools',113:'teiche-und-zubehoer',114:'tiermoebel',
       115:'zaeune-und-sichtschutz',116:'badgarnituren',117:'bettwaesche-und-laken',118:'decken-und-kissen',
       119:'fussmatten',120:'gardinen-und-vorhaenge',121:'handtuecher',122:'hussen-und-ueberwuerfe',
       123:'jalousien-und-rollos',124:'teppiche',125:'tischdecken-und-co',126:'babymoebel',127:'betten',128:'jugendzimmer',
       129:'kinderzimmerlampen',130:'regale',131:'schraenke',132:'schreibtische',133:'sessel-und-sofas',134:'dekoration',
       135:'komplett-kinderzimmer',136:'spielzeug',137:'stuehle',138:'textilien',139:'tische',140:'aussenlampen',
       141:'badlampen',142:'buerolampen',143:'deckenleuchten',144:'deckenventilatoren',145:'dekolampen',
       146:'kinderzimmerlampen',147:'lampenschirme-und-fuesse',148:'leuchtmittel',149:'stehlampen',
       150:'strahler-und-systeme',151:'taschenlampen',152:'tischleuchten',153:'wandlampen',154:'bettdecken-und-decken',
       155:'betten',156:'bettwaesche-und-laken',157:'kleiderschraenke',158:'kommoden',159:'kopfkissen',160:'lattenroste',
       161:'matratzen',162:'nachttische',163:'schlafsofas',164:'schlafzimmerlampen',165:'schlafzimmerserien',
       166:'teppiche',167:'bar-moebel',168:'Wohntextilien',169:'kamine-und-oefen',170:'polstermoebel',171:'regale',
       172:'schraenke',173:'sessel',174:'hocker-und-poufs',175:'sitzbaenke',176:'sofas',177:'stuehle',178:'teppiche',
       179:'tische',180:'truhen',181:'tv-hifi-moebel',182:'vitrinen',183:'wohnzimmerlampen',184:'zubehoer-fuer-moebel',
       185:'duscharmaturen',186:'duschkoepfe',187:'waschtischarmaturen',188:'schlaeuche',189:'badewannenarmaturen',
       190:'sonstige-badaccessoires',191:'haken',192:'haltegriffe',193:'handtuchhalter',194:'kosmetikeimer',
       195:'kosmetikspiegel',196:'seifenspender',197:'toilettenpapierhalter',198:'waagen',199:'wc-buersten',
       200:'eckbadewannen',201:'einbaubadewannen',202:'freistehende-badewannen',203:'wanneneinlagen',204:'whirlpools',
       205:'badgarnituren-sets',206:'badvorleger',207:'laeufer-und-matten',208:'badezimmerschraenke',
       209:'waschbeckenunterschraenke',210:'haengeschranke',211:'spiegelschraenke',212:'medizinschraenke',
       213:'unterschraenke',214:'badmoebel-sets',215:'badregale',216:'hocker',217:'duscharmaturen',218:'duschen',
       219:'duschhocker',220:'duschkoepfe',221:'duschvorhaenge',222:'duschwannen',223:'badetuecher',
       224:'gaestehandtuecher',225:'handtuch-sets',226:'saunatuecher',227:'saunaoefen',228:'sauna-textilien',
       229:'sauna-zubehoer',230:'saunen',231:'badspiegel',232:'kosmetikspiegel',233:'spiegelschraenke',234:'wc-becken',
       235:'wc-buersten',236:'wc-sitze',237:'armaturen',238:'badewannen-und-whirlpools',239:'durchlauferhitzer',
       240:'duschen',241:'sauna-und-zubehoer',242:'solarium',243:'waschbecken',244:'wcs',245:'aussenbelaege',
       246:'laminat',247:'parkett',248:'teppichboden',249:'campingmoebel',250:'feldbetten',251:'gaskocher',
       252:'luftmatratzen-und-isomatten',253:'schlafsaecke',254:'weiteres-campingzubehoer',255:'zelte',
       256:'dimmer',257:'lichtschalter',258:'steckdosen',259:'stromkabel',260:'verlaengerungskabel',261:'verteilerdosen',
       262:'weitere-kabel',263:'carports',264:'garagen',265:'garagentore',266:'durchlauferhitzer',267:'fussbodenheizungen',
       268:'heizgeraete',269:'heizungsanlagen',270:'klimageraete',271:'luftregulierer',272:'ventilatoren',
       273:'kaminbestecke',274:'kamine',275:'kaminholzkoerbe',276:'kaminzubehoer',277:'wandkamine',278:'aluleiter',
       279:'leitergeruest',280:'schiebeleiter',281:'stehleiter',282:'treppen',283:'trittleiter',284:'farben-und-lacke',
       285:'tapeten',286:'tapeziertische',287:'tapezierzubehoer',288:'baumaterialien',289:'daemmstoffe',290:'fenster',
       291:'rolllaeden',292:'tore',293:'trockenausbau',294:'tueren',295:'vordaecher',296:'bordueren',297:'fliesen',
       298:'verblendsteine',299:'wand-und-deckenverkleidungen',300:'bohrer-und-schrauber',301:'fraesen-und-schleifer',
       302:'hammer',303:'hobel-und-tacker',304:'saegen',305:'weitere-werkzeuge',306:'werkzeugkasten',307:'werkzeug-sets',
       308:'deckenleuchten',309:'schreibtischlampen',310:'stehlampen',311:'strahler-und-systeme',312:'buecherregale',
       313:'einzelregale',314:'haengeregale',315:'regalsysteme',316:'standregale',317:'wandregale',318:'aktenschraenke',
       319:'computerschraenke',320:'container',321:'haengeregistraturschraenke',322:'rollcontainer',323:'besucherstuehle',
       324:'buerostuehle',325:'chefsessel',326:'ergonomiestuehle',327:'konferenzstuehle',328:'zubehoer',329:'flipcharts',
       330:'haengetafeln',331:'computertische',332:'konferenztische',333:'schreibtische',334:'zubehoer',335:'dosen',
       336:'kaestchen',337:'korbwaren',338:'schalen',339:'truhen',340:'zeitungsstaender',341:'bilder',342:'poster',
       343:'rahmen',344:'blumenampeln',345:'blumenstaender',346:'kraenze',347:'kunstpflanzen',348:'pflanzen',
       349:'pflanzenkuebel',350:'afrika',351:'asien',352:'engel',353:'figuren',354:'tiere',355:'kerzen',
       356:'kerzenleuchter',357:'kerzenstaender',358:'laternen',359:'teelichter',360:'windlichter',361:'kosmetikspiegel',
       362:'standspiegel',363:'wandspiegel',364:'kissen',365:'teppiche-laeufer',366:'vorhaenge',367:'wohndecken',
       368:'kuckucksuhren',369:'standuhren',370:'wanduhren',371:'wecker',372:'bodenvasen',373:'tischvasen',
       374:'wallprints',375:'wanddekoration',376:'wandtattoos',377:'brotkasten',378:'etageren',379:'vorratsdosen',
       380:'barhocker',381:'bars',382:'barschraenke',383:'barzubehoer',384:'stehtische',385:'tresen-und-theken',
       386:'besteck',387:'geschirr',388:'glaeser',389:'kannen-und-wasserkessel',390:'karaffen',391:'dunstabzugshauben',
       392:'gefrierschraenke',393:'geschirrspuelmaschinen',394:'grillgeraete',395:'herde-und-backoefen',
       396:'kuehl-gefrier-kombis',397:'kuehlschraenke',398:'mikrowellen',399:'eckbankgruppen',400:'essgruppen',
       401:'gardinen',402:'gardinenstangen',403:'raffhalter',404:'scheibengardinen',
       405:'schiebegardinen-und-schiebevorhaenge',406:'schlaufenschals',407:'verdunklungsgardinen',408:'vorhaenge',
       409:'backformen',410:'kuechenhelfer',411:'kuechenwaagen',412:'pfannen',413:'toepfe',414:'jalousien',415:'plissees',
       416:'raffrollos',417:'seitenzugrollos',418:'springrollos',419:'verdunklungsrollos',420:'espressomaschinen',
       421:'kaffeemaschinen',422:'kaffeevollautomaten',423:'milchaufschaeumer',424:'teekocher',425:'kuechenzeilen',
       426:'minikuechen',427:'winkelkuechen',428:'entsafter',429:'fondue',430:'fritteusen',431:'kuechenmaschinen',
       432:'kuechenwaagen',433:'raclette',434:'ruehrgeraete-und-mixer',435:'toaster',436:'waffeleisen',437:'wasserfilter',
       438:'wasserkocher',439:'gewuerzregale',440:'standregale',441:'haengeregale',442:'weinregale',443:'kuchenschuerze',
       444:'tischdecken',445:'topflappen',446:'apothekerschraenke',447:'haengeschraenke',
       448:'kuechenbuffets-buffetschraenke',449:'spuelenschraenke',450:'umbauschraenke',451:'unterschraenke',
       452:'einfache-sitzbaenke',453:'eckbaenke',454:'sitztruhen',455:'truhenbaenke',456:'einbauspuelen',
       457:'spuelenarmaturen',458:'spuelenschraenke',459:'barhocker',460:'esszimmerstuehle',461:'freischwinger',
       462:'holzstuehle',463:'polsterstuehle',464:'klappstuehle',465:'kuechenhocker',466:'armlehnstuehle',467:'esstische',
       468:'kuechentische',469:'halter-und-haken',470:'muelleimer',471:'garderobenbaenke',472:'garderobenhaken',
       473:'garderobenpaneele',474:'garderobenschraenke',475:'garderoben-sets',476:'garderobenstaender',
       477:'kleiderbuegel',478:'buegelbretter',479:'buegeleisen',480:'dampfreiniger',481:'staubsauger',
       482:'strick-und-naehmaschinen',483:'deckenleuchten',484:'dekolampen',485:'stehlampen',486:'strahler-und-systeme',
       487:'wandlampen',488:'standregale',489:'wandregale',490:'schuhkommoden',491:'schuhregal',492:'schuhschraenke',
       493:'garderobenspiegel',494:'standspiegel',495:'wandspiegel',496:'aussenstrahler',497:'bodeneinbauleuchten',
       498:'gartenleuchten',499:'hausnummern',500:'sockelleuchten',501:'solarleuchten',502:'wandleuchten',
       503:'wasserleuchten',504:'wegeleuchten',505:'balkon-beleuchtung',506:'balkon-bodenbelaege',507:'balkondekoration',
       508:'balkonpflanzen',509:'balkon-sets',510:'balkonstuehle',511:'balkontische',512:'grill-und-zubehoer',
       513:'pflanzenkaesten',514:'sichtschutz',515:'sonnenschutz',516:'dekofiguren',517:'gartenzwerge',518:'windmuehlen',
       519:'windraeder',520:'windspiele',521:'beile',522:'hacken',523:'heckenscheren',524:'laubsauger-und-haecksler',
       525:'rasentrimmer',526:'spaten-und-schaufeln',527:'vertikutierer',528:'aufbewahrung',529:'gartenbaenke',
       530:'gartenliegen',531:'gartenmoebel-set',532:'gartenstuehle',533:'gartentische',534:'hollywoodschaukeln',
       535:'loungemoebel-garten',536:'outdoor-sitzsaecke',537:'schutzhuellen',538:'sitzauflagen',539:'sonneninseln',
       540:'sonnenschirme',541:'sonnenschirme-und-markisen',542:'sonnenschirmstaender',543:'feuerstellen',
       544:'gartenkamine',545:'grillgeraete',546:'grillzubehoer',547:'blumentoepfe',548:'duenger',549:'pflanzen',
       550:'pflanzkaesten',551:'markisen',552:'sonnenschirme',553:'sonnenschirmstaender',554:'sonnensegel',
       555:'sonneninseln',556:'strandkoerbe',557:'filteranlagen',558:'poolpflege',559:'schwimmbecken',560:'zubehoer',
       561:'hasenstaelle-kaninchenstaelle',562:'hundekoerbe-hundebetten',563:'katzenkoerbe',564:'vogelhaeuser-vogelbaeder',
       565:'vogelkaefige-volieren',566:'badgarnituren-set',567:'badvorleger',568:'laeufer-und-matten',569:'bettlaken',
       570:'bettwaesche-garnituren',571:'kinderbettwaesche',572:'kopfkissenbezuege',573:'matratzenschoner',
       574:'wendebettwaesche',575:'baumwolldecken',576:'bettdecken',577:'kissen',578:'kopfkissen',579:'mehr-decken',
       580:'naturfaserdecken',581:'tagesdecken-und-bettueberwuerfe',582:'gardinen',583:'gardinenstangen',584:'raffhalter',
       585:'scheibengardinen',586:'schiebegardinen-und-schiebevorhaenge',587:'schlaufenschals',588:'verdunklungsgardinen',
       589:'vorhaenge',590:'badetuecher',591:'gaestehandtuecher',592:'handtuch-set',593:'saunatuecher',
       594:'baendchenrollos',595:'jalousien',596:'plissees',597:'raffrollos',598:'seitenzugrollos',599:'springrollos',
       600:'verdunklungsrollos',601:'berberteppiche',603:'bruecken-teppiche',604:'hochflorteppiche',605:'kinderteppiche',
       606:'laeufer',607:'orientteppiche',608:'sonstige-teppiche',609:'teppichboden',610:'wandteppich',611:'platz-sets',
       612:'servietten',613:'tischdecken',614:'tischlaeufer',615:'tisch-sets',616:'komplett-babyzimmer',617:'laufgitter',
       618:'wickelkommoden',619:'babybetten',620:'baldachine',621:'etagenbetten',622:'hochbetten',623:'kinderbetten',
       624:'jugendbetten',625:'komplett-jugendzimmer',626:'schraenke',627:'stuehle',628:'tische',629:'holzspielzeug',
       630:'kartenspiele',631:'kinderfahrraeder',632:'puppen',633:'sandkaesten',634:'schaukeln-und-rutschen',
       635:'sonstiges-spielzeug',636:'spielzeugkisten',637:'stofftiere',638:'trampoline',639:'uhren',640:'hochstuehle',
       641:'kinderstuehle',642:'schreibtischstuehle',643:'babytextilien',644:'handtuecher',645:'kinderbettwaesche',
       646:'kinderkissen',647:'kinderteppiche',648:'schreibtische',649:'spieltische',650:'aussenstrahler',
       651:'bodeneinbauleuchten',652:'gartenleuchten',653:'hausnummern',654:'sockelleuchten',655:'solarleuchten',
       656:'wandleuchten',657:'wasserleuchten',658:'wegeleuchten',659:'deckenleuchten',660:'schreibtischlampen',
       661:'deckenlampen',662:'kronleuchter',663:'pendelleuchten',664:'lampenfuesse',665:'lampenschirme',
       666:'energiesparlampen',667:'halogenstrahler',668:'led',669:'leuchtstoffroehren',670:'mehr-leuchtmittel',
       671:'deckenfluter',672:'standleuchten',673:'einbaustrahler',674:'moebelaufbaustrahler',675:'schienensysteme',
       676:'seilsysteme',677:'strahler-und-spots',678:'beistelltischlampen',679:'kugelleuchten',680:'leseleuchten',
       681:'nachttischlampen',682:'daunendecken',683:'4-jahreszeiten-decken',684:'tagesdecken-und-bettueberwuerfe',
       685:'unterbetten',686:'bettschubkaesten',687:'boxspringbetten',688:'doppelbetten',689:'funktionsbetten',
       690:'futonbetten',691:'gaestebetten',692:'himmelbetten',693:'hochbetten',694:'kinderbetten',695:'komfortbetten',
       696:'landhausbetten',697:'luftbetten',698:'metallbetten',699:'polsterbetten',700:'rattanbetten',701:'rundbetten',
       702:'schrankbetten',703:'wasserbetten',704:'bettlaken',705:'bettwaesche-garnituren',706:'kinderbettwaesche',
       707:'kopfkissenbezuege',708:'matratzenschoner',709:'wendebettwaesche',710:'drehtuerenschraenke',
       711:'ordnungssysteme',712:'schwebetuerenschraenke',713:'wandschraenke',714:'nachttischkommoden',
       715:'schminkkommoden-und-schminktische',716:'waeschekommode',717:'kopfkissen',718:'kopfkissenbezuege',
       719:'nackenstuetzkissen',720:'elektrische-lattenroste',721:'rollroste',722:'unverstellbare-lattenroste',
       723:'verstellbare-lattenroste',724:'boxspringmatratzen',725:'federkernmatratzen',726:'gelmatratzen',
       727:'kaltschaum-matratzen',728:'latexmatratzen',729:'matratzenschoner',730:'matratzen-sets',731:'naturmatratzen',
       732:'taschenfederkern',733:'unterbetten',734:'viscoschaum-matratzen',735:'weitere-matratzen',736:'polsterliegen',
       737:'schlafsessel',738:'deckenleuchten',739:'dekolampen',740:'kugelleuchten',741:'lampenschirme-und-fuesse',
       742:'leseleuchten',743:'leuchtmittel',744:'nachttischlampen',745:'stehlampen',746:'strahler-und-systeme',
       747:'wandlampen',748:'bettvorleger',749:'hochflor-teppiche',750:'laeufer',751:'teppichboden',752:'barhocker',
       753:'bars',754:'barschraenke',755:'barzubehoer',756:'stehtische',757:'tresen-und-theken',758:'dekokissen',
       759:'gardinen-und-vorhaenge',760:'hussen-und-ueberwuerfe',761:'jalousien-und-rollos',762:'kaminbestecke',
       763:'kamine',764:'kaminholzkoerbe',765:'kaminzubehoer',766:'wandkamine',767:'2-und-3-sitzer-sofas',768:'bigsofas',
       769:'polsterecken',770:'polstergarnituren',771:'polsterhocker',772:'recamieren',773:'schlafsofas',
       774:'wohnlandschaften',775:'buecherregale',776:'einzelregale',777:'haengeregale',778:'mehrzweckregale',
       779:'raumteiler',780:'regalsysteme',781:'regalwuerfel',782:'haengeschraenke',783:'highboards',784:'kommoden',
       785:'lowboards',786:'sideboards',787:'wandschraenke',788:'weitere-schraenke',789:'wohnwaende',
       790:'chesterfield-sessel',791:'clubsessel',792:'fernsehsessel',793:'massagesessel',794:'ohrensessel',
       795:'rattansessel',796:'relaxliegen',797:'relaxsessel',798:'schaukelsessel',799:'schlafsessel',800:'schwingsessel',
       801:'sitzsaecke',802:'polsterhocker',803:'poufs',804:'sitzhocker',805:'sitzwÃ¼rfel',806:'eckbaenke',
       807:'sitztruhen',808:'truhenbaenke',809:'2-und-3-sitzer-sofas',810:'bigsofas',811:'chesterfield-sofa',
       812:'ecksofas-eckcouches',813:'recamieren',814:'schlafsofas',815:'wohnlandschaften',816:'garnituren',
       817:'freischwinger',818:'hocker',819:'schaukelstuehle',820:'wohnzimmerstuehle',821:'hochflorteppiche',822:'laeufer',
       823:'orientteppiche',824:'sonstige-teppiche',825:'wandteppich',826:'beistelltische',827:'couchtische',
       828:'esstische',829:'glastische',830:'konsolentische',831:'satztische',832:'tischdecken-und-co',833:'truhentische',
       834:'weitere-tische',835:'cd-dvd-regale',836:'hifi-racks',837:'hifi-zubehoer',838:'staender-standfuesse',
       839:'tv-halterungen',840:'tv-lowboards',841:'tv-racks',842:'tv-schraenke',843:'tv-waende',844:'eckvitrinen',
       845:'glasvitrinen',846:'haengevitrinen',847:'sammlervitrinen',848:'standvitrinen',849:'deckenleuchten',
       850:'dekolampen',851:'lampenschirme-und-fuesse',852:'leuchtmittel',853:'stehlampen',854:'strahler-und-systeme',
       855:'tischleuchten',856:'wandlampen',857:'moebelpflege',858:'komplett-schlafzimmer',859:'massivholzbetten',
       860:'loungesessel',861:'sitzbadewannen',862:'duschen',863:'waschmaschinen-und-trockner',864:'ablufttrockner',
       865:'einbauwaschmaschinen',866:'frontlader',867:'kondenstrockner',868:'toplader',869:'waermepumpentrockner',
       870:'waschtrockner',871:'zubehoer',872:'weihnachten',873:'adventskranz-leuchter',874:'christbaumschmuck',
       875:'geschenkideen',876:'weihnachtsbeleuchtung',877:'weihnachtsdeko'}

#Grab the category ids to use in download process
categories=image_urls['category_id'].value_counts().index.tolist()


# This code will grab all the urls in df and download randomly selected 150 files per each category
for i in categories:
    e=0 # counter for total processed files
    print("Processing catecory %d..." %i)
    if len(list(image_urls[image_urls['category_id']==i]['image_url']))>150:
        for x in random.sample(list(image_urls[image_urls['category_id']==i]['image_url']),150):
            try:
                y=''.join(re.findall('(?:http\:|https\:)?\/\/.*\.(?:png|jpg|giff|bmp|img)', x))
                if not y:
                    y=x
                if y.endswith(('.jpg', '.png','.giff','.bmp','.img'))== False:
                    file_name = "{}.{}_".format(i,names[i]) +"_%s"%e + y.split('/')[-1] +'.jpg'
                else:
                    file_name = "{}.{}_".format(i,names[i]) +"_%s"%e +  y.split('/')[-1]
                fullfilename = os.path.join('D:/PROJECTS/LadenDirekt/{}.{}/'.format(i,names[i]), file_name)
                if not os.path.isdir('D:/PROJECTS/LadenDirekt/{}.{}/'.format(i,names[i])):
                    os.makedirs('D:/PROJECTS/LadenDirekt/{}.{}/'.format(i,names[i]))
                urllib.request.urlretrieve(y, fullfilename)
                e+=1
            except Exception:
                continue
        print ('For Category {} there were {} total files executed'.format(i,e))
    else:
        for x in random.choices(list(image_urls[image_urls['category_id']==i]['image_url']),k=150):
            try:
                y=''.join(re.findall('(?:http\:|https\:)?\/\/.*\.(?:png|jpg|giff|bmp|img)', x))
                if not y:
                    y=x
                if y.endswith(('.jpg', '.png','.giff','.bmp','.img'))== False:
                    file_name = "{}.{}_".format(i,names[i]) +"_%s"%e + y.split('/')[-1] +'.jpg'
                else:
                    file_name = "{}.{}_".format(i,names[i]) +"_%s"%e +  y.split('/')[-1]
                fullfilename = os.path.join('D:/PROJECTS/LadenDirekt/{}.{}/'.format(i,names[i]), file_name)
                if not os.path.isdir('D:/PROJECTS/LadenDirekt/{}.{}/'.format(i,names[i])):
                    os.makedirs('D:/PROJECTS/LadenDirekt/{}.{}/'.format(i,names[i]))
                urllib.request.urlretrieve(y, fullfilename)
                e+=1
            except Exception:
                continue
        print ('For Category {} there were {} total files executed'.format(i,e))