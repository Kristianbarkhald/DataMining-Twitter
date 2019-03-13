import csv, sys, re, tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
#Her legger vi vi access nøkkelene vi får av Twitter
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

#auth er er autorisering som vi gir consumer key og consumer secret.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#Lager en variabel for hvilken hashtag vi vil hente.
film = "BohemianRhapsody"
#Vi åpner en csv fil, og hvis filen ikke eksisterer blir den opprettet. Der sier vi ifra at vi skal skrive til filen, w overskriver hva som ligger i filen fra før.
csvFile = open(film+'.csv', 'w', newline='')
#Bruker csvWriter for å skrive til filen vi laget.
csvWriter = csv.writer(csvFile)
#Setter inn titler på kolonnene i første rad.
csvWriter.writerow(['Dato', 'Tekst', 'Polaritet', 'Resultat'])
#Vi lager to variabler, den første er det offesielle hastaggen til filmen på twitter. Og den andre er hvilke ord vi vil søke etter.
#I dette tilfellet så vi at noen bare tagger mange kjente filmer for å reklamere en VPN tjeneste. Disse tweetene kan vi filtrere bort ved å bruke -VPN

#I dette tilfellet velger vi å hente ut søkeordet was for å få tweets somgir en mening om filmen, enten positiv, nøytral eller negativ.
keyword = "was -VPN"
#Setter opp en variabel for hvor mange tweets vi skal hente ut.
antallTweets = 500
polaritet = 0
positiveTweets = 0
vpositiveTweets = 0
lpositiveTweets = 0
negativeTweets = 0
vnegativeTweets = 0
lnegativeTweets = 0
nøytrale = 0
resultat =  ""
#Sjekker hver tweet og henter ut publiseringsdato og tweetens innhold.
#tweepyCursor tar her imot: søkeord, språk, fra dato og hele tweet teksten. Den henter i dette eksemplet 500 tweets.
#api_search bruker vi for å hente ut søkeordene vi vil ha og for å filtrere ut retweets.
#Vi spesifiserer også hvor langt tilbake vi skal hente tweetene, men etter nærmere analyse virker det som vi bare kan hente opptil 10 dager bakover av gangen.
#tweetene blir lagret i en CSV fil med tre kolonner: dato, innhold og resultat.
#Bruker TextBlob til å analysere teksten i tweeten.
#Velger grensene for nøyansene vi bruker. alt under 0 er negativt, vi velger å lage flere grupper enn bare positiv/nøytral/negativ.
#Vi lager en variabel vi kaller resultat som viser med ord hvor positiv/negativ tweeten er. Dette legger vi inn i csv filen så det er mulig å forstå filen hvis en vil se rådataen.
for tweet in tweepy.Cursor(api.search,q="#"+film+" "+keyword+"  -filter:retweets",
                           lang="en",
                           since="2018-11-05",tweet_mode='extended').items(antallTweets):

    analyse = TextBlob(tweet.full_text)
    if (analyse.sentiment.polarity == 0):#Er den 0 er den helt nøytral.
        nøytrale += 1
        resultat="nøytral"
    elif (analyse.sentiment.polarity > 0 and analyse.sentiment.polarity <= 0.3): #større enn 0 og mindre eller lik 0.3 er litt positivt.
        lpositiveTweets += 1
        resultat="litt positiv"
    elif (analyse.sentiment.polarity > 0.3 and analyse.sentiment.polarity <= 0.6):#større enn 0.3 og mindre eller lik 0.6 er positivt.
        positiveTweets += 1
        resultat="positiv"
    elif (analyse.sentiment.polarity > 0.6 and analyse.sentiment.polarity <= 1):#større enn 0.6 og mindre eller lik 1 er veldig positivt.
        vpositiveTweets += 1
        resultat="veldig positiv"
    elif (analyse.sentiment.polarity > -0.3 and analyse.sentiment.polarity < 0):#større enn -0.3 og mindre enn 0 er litt negativt.
        lnegativeTweets += 1
        resultat="litt negativ"
    elif (analyse.sentiment.polarity > -0.6 and analyse.sentiment.polarity <= -0.3):#større enn -0.6 og mindre eller lik -0.3 er negativt.
        negativeTweets += 1
        resultat="negativ"
    elif (analyse.sentiment.polarity >= -1 and analyse.sentiment.polarity <= -0.6):#større eller lik -1 og mindre eller lik -0.6 er veldig negativt.
        vnegativeTweets += 1
        resultat="veldig negativ"
    csvWriter.writerow([tweet.created_at, re.sub("[^A-Za-z]", " ", tweet.full_text), analyse.sentiment.polarity, resultat])





#Vi lager en funksjon som tar to parametere: første tallet er antall positive/nøytrale/negative tweets og det andre er antall tweets vi har totalt.
#Vi finner prosenten ved å gange 100 med antall positive/nøytrale/negative tweets og deler det på antall totale tweets.
#Vi formaterer temp til å kun ha to desimaler.
def prosent(part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')


#Vi gjør om fra desimaler til prosent ved å bruke funksjonen vi laget over.
positiveTweets = prosent(positiveTweets, antallTweets)
vpositiveTweets = prosent(vpositiveTweets, antallTweets)
lpositiveTweets = prosent(lpositiveTweets, antallTweets)
negativeTweets = prosent(negativeTweets, antallTweets)
vnegativeTweets = prosent(vnegativeTweets, antallTweets)
lnegativeTweets = prosent(lnegativeTweets, antallTweets)
nøytrale = prosent(nøytrale, antallTweets)

#Lager to variabler der den første tar summen av alle de positive tweetene, og den andre tar summen av de negative.
#Variablene blir formatert til å ha to desimaler.
sum_positiv = format(float(positiveTweets) + float(vpositiveTweets) + float(lpositiveTweets), '.2f')
sum_negativ = format(float(negativeTweets) + float(vnegativeTweets) + float(lnegativeTweets), '.2f')

#Printer ut en rapport i konsollvinduet.
print()
print("Detaljert rapport: ")
print(str(positiveTweets) + "% skrev positive tweets om filmen")
print(str(vpositiveTweets) + "% skrev veldig positive tweets om filmen")
print(str(lpositiveTweets) + "% skrev litt positive tweets om filmen")
print(str(negativeTweets) + "% skrev negative tweets om filmen")
print(str(vnegativeTweets) + "% skrev veldig negative tweets om filmen")
print(str(lnegativeTweets) + "% skrev litt negative tweets om filmen")
print(str(nøytrale) + "% skrev nøytrale tweets om filmen")

#Lager figur 1
#Kaller figuren figur1. Legger på navn, farge. Vi legger størrelsen på kakeandelene til antall positive/negative tweets.
#Vi lager også en patch som er en rektangel, brukes som en ramme.
#Bruker patcher for å få det mer oversiktelig.
#startangle er vinkelen diagrammed skal starte i, og vi legger også på en skygge.
#En legend er navnene på delene med tilsvarende fargekode på en liste nedover.
#loc er plassering
#axis er skalering, den vil holde seg som en sirkel
#Vi legger til en tittel som viser hastaggen vi søker etter og antallet tweets
#tight layout gjør at det er plass til alt på skjermen.
plt.figure(1)
labels = 'Litt positive '+ str(lpositiveTweets)+'%', 'Positive '+ str(positiveTweets)+'%', 'Veldig positive '+ str(vpositiveTweets)+'%', 'Nøytrale '+ str(nøytrale)+'%', 'Litt negative '+ str(lnegativeTweets)+'%', 'Negative '+ str(negativeTweets)+'%', 'Veldig negative '+ str(vnegativeTweets)+'%'
sizes = [lpositiveTweets, positiveTweets, vpositiveTweets, nøytrale, lnegativeTweets, negativeTweets, vnegativeTweets]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'darkgreen', 'purple', 'red']
patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title('Detaljert oversikt på #' + film + ' ved å analysere ' + str(antallTweets) + ' tweets.')
plt.axis('equal')
plt.tight_layout()
#Vi gjør det samme på figur to, men velger bare tre biter.
plt.figure(2)
labels = 'Positive '+ str(sum_positiv)+'%', 'Nøytrale '+ str(nøytrale)+'%', 'Negative '+ str(sum_negativ)+'%'
sizes = [sum_positiv, nøytrale, sum_negativ]
colors = ['yellowgreen', 'lightskyblue', 'purple']
patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title('Enkel oversikt på #' + film + ' ved å analysere ' + str(antallTweets) + ' tweets.')
plt.axis('equal')
plt.tight_layout()
plt.show()
