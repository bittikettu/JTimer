# -*- coding: utf-8 -*-
import json
class kilpailija:
    def __init__(self,etunimi,sukunimi,puhelinnumero,seura,kilpasarja,bibnumber):
        self.etunimi = etunimi
        self.sukunimi = sukunimi
        self.puhelinnumero = puhelinnumero
        self.seura = seura
        self.kilpasarja = kilpasarja
        self.bibnumber = bibnumber
        self.ajat = []
        self.valiajat = []
        self.valiaikamaara = 0
        self.maaliintuloaika = 0
        self.sijoitus = 9999
        self.dnf = False
        self.dns = False
        self.dsq = False
        self.lasttime = 0
        self.totaltime = 9999999999
        self.plusrounds = 0



    def __str__(self):
        if(self.sijoitus == 9999):
            return ('%s, %s %s, %s, %s' % (self.bibnumber, self.etunimi, self.sukunimi, self.seura, self.kilpasarja))
        else:
            return ('%s, %s %s, %s, %s, %d' % (self.bibnumber, self.etunimi, self.sukunimi, self.seura, self.kilpasarja,self.sijoitus))
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,ensure_ascii=True)#return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def kirjaaAika(self,aika,valiaikamaara):
        self.ajat.append(aika)
        self.lasttime = aika
        if valiaikamaara != self.valiaikamaara:
            self.valiaikamaara = self.valiaikamaara + 1
        #print(int((aika-int(aika))*100))
        if len(self.valiajat) == 0:
            self.valiajat.append(aika)
            self.totaltime = self.valiajat[0]
        else:
            #print(len(self.ajat))
            self.valiajat.append(aika - self.ajat[len(self.ajat)-2])
            self.totaltime = self.totaltime + self.valiajat[len(self.valiajat)-1]
        print(self.toJSON())

    def clear(self):
        self.ajat.clear()
        self.valiajat.clear()
        self.valiaikamaara = 0
        self.maaliintuloaika = 0
        self.sijoitus = 9999
        self.dnf = False
        self.dns = False
        self.dsq = False
        self.lasttime = 0
        self.totaltime = 9999999999
        self.plusrounds = 0

    def Sijoitus(self,sijoitus):
        self.sijoitus = sijoitus

    def DNF(self):
        if self.dnf == False:
            self.dnf = True
        else:
            self.dnf = False
    
    def DNS(self):
        if self.dns == False:
            self.dns = True
        else:
            self.dns = False

    def DISQUALIFY(self):
        if self.dsq == False:
            self.dsq = True
        else:
            self.dsq = False

    def getStatus(self):
        if self.dnf == True:
            return "DNF"
        elif self.dns == True:
            return "DNS"
        elif self.dsq == True:
            return "DSQ"
        else:
            return ""
    
    def isStatusOn(self):
        if self.dnf or self.dns or self.dsq:
            self.toJSON()
            return True
        else:
            self.toJSON()
            return False

    def Plusrounds(self,rounds):
        self.plusrounds = rounds

    def GetTimeAmount(self):
        return len(self.ajat)
