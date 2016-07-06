import os
import feedparser
import urllib
import urllib.request
from XMLCSV.csv_import import CSVfeed


class XMLdata:

    def __init__(self,url):
        self.url = url
        self.d = feedparser.parse(url)
        self.link_p = self.d.feed.title_detail.base
        self.title_p = self.d.feed.title_detail.value
        self.url_site = self.d.feed.link
    
    def add_feed(self):

        CSV = CSVfeed()
        CSV.new_feed(self.title_p,self.link_p)

    def feed_in(self):

        if str.find(self.url, "http://") != False:
            self.url = "http://" + self.url
        print("Loading feed...")

        n_epsodes = int((len(self.d['entries'])))
        return self.d, n_epsodes

    def download(self, name, file, podcast_name):

        html = urllib.request.urlopen(file).read()
        name = name + ".mp3"
        print(file)
        #remove / filename
        if str.find(name, ","):
            name = name.replace('/','')

        d = ('PodCast/' + podcast_name + '/')

        if not os.path.exists(d):
            os.makedirs(d)

        arq = open(d + name, "wb")
        arq.write(html)
        arq.close()

    def clear_link(self, mp3):
        mp3 = mp3.split(".mp3")[0]
        mp3 = mp3.split("http://")[-1]

        if str.find(mp3, "http://") != 0:
            mp3 = "http://" + mp3

        if str.find(mp3, ".mp3") == -1:
            mp3 = mp3 + ".mp3"

        return mp3

    def search_pod(self, feed, search):
        d, n_epsodes = feed
        list_q = {}
        quant_episodes = 0
        error_search = 0

        for i in range(n_epsodes):
            titulo = (d['entries'][i]['title'])

            if str.find(str.upper(titulo), str.upper(search)) != -1:

                search_value = i
                list_q[int(quant_episodes)] = i
                quant_episodes += 1

                print("|{}|".format(i), "\t{}".format(d['entries'][i]['title']))

        if quant_episodes > 1:

            choice = input("Insert Episode ID: ")

            for quant in range(0, quant_episodes):

                if list_q[quant] == choice:
                    search_value = int(choice)

        elif quant_episodes < 1:

            error_search = 1
            mp3 = None
            name = None

        if error_search != 1:

            mp3 = str(d['entries'][search_value]['enclosures'])
            name = str(d['entries'][search_value]['title'])

        return mp3, name, error_search