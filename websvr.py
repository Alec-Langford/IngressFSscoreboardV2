import spelling
from peewee import *
import requests
from cherrypy.lib.static import serve_file
from mako.template import Template
from mako.lookup import TemplateLookup
import cherrypy.process.plugins
import cherrypy

class DBM():
    def __init__(self):
        self.db = SqliteDatabase(':memory:', threadlocals=True)

dbm = DBM()


class player_begin(Model):

    PlayerName = CharField(unique=True)
    Faction = CharField(unique=False)
    StartLevel = IntegerField()
    StartAP = IntegerField()
    StartStat1 = IntegerField()
    StartStat2 = IntegerField()

    class Meta:
        database = dbm.db

class player_end(Model):

    PlayerName = CharField(unique=True)
    EndLevel = IntegerField()
    EndAP = IntegerField()
    EndStat1 = IntegerField()
    EndStat2 = IntegerField()

    class Meta:
        database = dbm.db

class player(Model):
    PlayerName = CharField(unique=True)
    Faction = CharField(unique=False)
    DiffLevel = IntegerField()
    DiffAP = IntegerField()
    DiffStat1 = IntegerField()
    DiffStat2 = IntegerField()

    class Meta:
        database = dbm.db




class DataMGR():
    def __init__(self,stat1="Kms",stat2="Hacks"):
        self.template_url = "https://docs.google.com/spreadsheets/d/%s/export?format=csv"
        signinurl = "https://docs.google.com/spreadsheets/d/1b6hcUfZv4JO1qNxPMsWm0eiVuuaF0JIndlijvzCYDhM/pubhtml"
        signouturl = "https://docs.google.com/spreadsheets/d/1n6m-QXZeZ15JczhNsc5c8hO-44DOOgB1cEU96BlvgMY/pubhtml"
        self.signin = ''
        self.signout = ''
        self.urls = [signinurl, signouturl]
        self.correct_users = ''
        self.begin = ['PlayerName','Faction','StartLevel','StartAP','StartStat1','StartStat2']
        self.end = ["PlayerName","EndLevel","EndAP","EndStat1","EndStat2"]
        self.joined = ["PlayerName","Faction", "DiffLevel" ,"DiffAP" ,"DiffStat1","DiffStat2"]
        self.stat1 = stat1
        self.stat2 = stat2
        self.scoreboard = []

    def get_key(self,x):
        x = x[39:].split("/")
        return x[0]

    def get_data(self,url):
        response = requests.get(url)
        return response.text.split("\n")[1:]

    def collect(self):
        try:
            dbm.db.create_tables([player_begin, player_end, player])
        except OperationalError:
            pass
        t=[]
        for item in self.urls:
            i = self.template_url%self.get_key(item)
            t.append(self.get_data(i))
        self.signin, self.signout = t


        for item in self.signin:
            item = item.split(",")
            self.correct_users+=(item[1]+"\n")
            i=[item[1].lower(),item[2]]+map(int,item[3:])
            try:
                c = player_begin.create(**dict(zip(self.begin, i)))
            except IntegrityError:
                pass
        correct = spelling.main(self.correct_users)

        for item in self.signout:
            item = item.split(",")
            i = [correct(item[1]), ]+ map(int,item[2:])
            try:
                c = player_end.create(**dict(zip(self.end, i)))
            except IntegrityError:
                pass

    def join_tables(self):
        f=player._meta.get_field_names()[1:]
        for item in player_begin.raw("select * from player_begin LEFT JOIN player_end ON player_begin.PlayerName=player_end.PlayerName"):
            try:
                r=[item.PlayerName, item.Faction, item.EndLevel-item.StartLevel, item.EndAP-item.StartAP, item.EndStat1-item.StartStat1, item.EndStat2-item.StartStat2]
                c = player.create(**dict(zip(self.joined, r)))
            except TypeError:
                pass

        qry = player.select().order_by(player.DiffLevel.desc(), player.DiffAP.desc())
        results=open("scoreboard.csv","w")
        self.scoreboard=[]
        for item in qry:
            x=[str(getattr(item,i)) for i in f]
            results.write(",".join(x)+"\n")
            self.scoreboard.append(x)
        results.close()
        #print self.scoreboard

        qry1 = player.select().where(player.Faction=="Enlightened")
        enlightened_counted = qry1.count()
        if enlightened_counted ==0:
            enlightened_counted+=1
        enlightened_average = sum([item.DiffAP for item in qry1])/enlightened_counted
        enlightened_total = sum([item.DiffAP for item in qry1] )
        enlightened_levels = sum([item.DiffLevel for item in qry1] )
        enlightened_stat1_total = sum([item.DiffStat1 for item in qry1] )
        enlightened_stat1_avg = sum([item.DiffStat1 for item in qry1] )/enlightened_counted
        enlightened_stat2_total = sum([item.DiffStat1 for item in qry1] )
        enlightened_stat2_avg = sum([item.DiffStat1 for item in qry1] )/enlightened_counted

        qry1 = player.select().where(player.Faction=="Resistance")
        resistance_counted = qry1.count()
        if resistance_counted == 0:
            resistance_counted +=1
        resistance_average = sum([item.DiffAP for item in qry1])/resistance_counted
        resistance_total = sum([item.DiffAP for item in qry1] )
        resistance_levels = sum([item.DiffLevel for item in qry1] )
        resistance_stat1_total = sum([item.DiffStat1 for item in qry1] )
        resistance_stat1_avg = sum([item.DiffStat1 for item in qry1] )/enlightened_counted
        resistance_stat2_total = sum([item.DiffStat2 for item in qry1] )
        resistance_stat2_avg = sum([item.DiffStat2 for item in qry1] )/enlightened_counted

        d={
            "e_players": enlightened_counted,
            "e_average": enlightened_average,
            "e_total": enlightened_total,
            "e_levels": enlightened_levels,
            "e_stat1_total": enlightened_stat1_total,
            "e_stat1_avg": enlightened_stat1_avg,
            "e_stat2_total": enlightened_stat2_total,
            "e_stat2_avg": enlightened_stat2_avg,


            "r_players": resistance_counted,
            "r_average": resistance_average,
            "r_total": resistance_total,
            "r_levels": resistance_levels,
            "r_stat1_total": resistance_stat1_total,
            "r_stat1_avg": resistance_stat1_avg,
            "r_stat2_total": resistance_stat2_total,
            "r_stat2_avg": resistance_stat2_avg,


            "g_scoreboard": self.scoreboard,
            "g_players": sum([enlightened_counted,resistance_counted]),
            "g_stat1Name":self.stat1,
            "g_stat2Name":self.stat2,
            "g_stat1_total":sum([resistance_stat1_total,enlightened_stat1_total]),
            "g_stat2_total":sum([resistance_stat2_total,enlightened_stat2_total]),

        }

        [item.delete() for item in player.select()]
        [item.delete() for item in player_begin.select()]
        [item.delete() for item in player_end.select()]
        #print player.select()



        return d

    def update_scoreboard(self):
        self.collect()
        d=self.join_tables()
        return d

d=DataMGR()

class cache:
    def __init__(self):
        self.value = d.update_scoreboard()

    def update(self):

        self.value = d.update_scoreboard()
        print "updated"


c=cache()

class WebApp(object):
    def __init__(self):
        #d.collect()
        self.lookup = TemplateLookup(directories=["/"])

    @cherrypy.expose
    def index(self):
        r = c.value
        t = Template(filename="index.mako",lookup=self.lookup)
        return t.render(**r)

    @cherrypy.expose
    def stats(self):
        r = c.value
        t = Template(filename="stats.mako",lookup=self.lookup)
        return t.render(**r)



    @cherrypy.expose
    def sitrep(self):

        t = Template(filename="sitrep.mako", lookup=self.lookup)
        r=c.value
        return t.render(**r)



if __name__ == '__main__':

    wd = cherrypy.process.plugins.BackgroundTask(30,c.update)
    wd.start()

    cherrypy.quickstart(WebApp(), '/', 'c.conf')
























