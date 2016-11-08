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
        self.lasttime = 0
        self.totaltime = 9999999999



    def __str__(self):
        if(self.sijoitus == 9999):
            return ('%s, %s %s, %s, %s' % (self.bibnumber, self.etunimi, self.sukunimi, self.seura, self.kilpasarja))
        else:
            return ('%s, %s %s, %s, %s, %d' % (self.bibnumber, self.etunimi, self.sukunimi, self.seura, self.kilpasarja,self.sijoitus))
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,ensure_ascii=True)#return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    '''def syotatiedot(self):
        #os.system("cls")
        self.etunimi = input("Etunimi: ")
        self.sukunimi = input("Sukunimi: ")
        self.puhelinnumero = input("puhelinnumero: ")
        self.seura = input("seura: ")
        self.kilpasarja = input("kilpasarja: ")
        self.bibnumber = int(input("Sukunimi: "))'''

    def kirjaaAika(self,aika):
        self.ajat.append(aika)
        self.lasttime = aika
        self.valiaikamaara = self.valiaikamaara + 1
        #print(int((aika-int(aika))*100))
        if len(self.valiajat) == 0:
            self.valiajat.append(aika)
            self.totaltime = self.valiajat[0]
        else:
            #print(len(self.ajat))
            self.valiajat.append(aika - self.ajat[len(self.ajat)-2])
            self.totaltime = self.totaltime + self.valiajat[len(self.valiajat)-1]
        #print(self.ajat)
        #print(self.valiajat)
        #print(self.totaltime)

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
            

    def GetTimeAmount(self):
        return len(self.ajat)
