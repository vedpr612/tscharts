# -*- coding: utf-8 -*-
#(C) Copyright Syd Logan 2017
#(C) Copyright Thousand Smiles Foundation 2017
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import unittest
import getopt, sys
import json
from datetime import datetime, timedelta
from random import randint
import time
import threading
import base64

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.clinic.clinic import CreateClinic, DeleteClinic
from test.queue.queue import GetQueue, DeleteQueueEntry
from test.category.category import CreateCategory
from test.image.image import CreateImage
from test.station.station import CreateStation, DeleteStation, GetStation
from test.patient.patient import CreatePatient, DeletePatient
from test.medicalhistory.medicalhistory import CreateMedicalHistory, DeleteMedicalHistory
from test.statechange.statechange import CreateStateChange
from test.clinicstation.clinicstation import CreateClinicStation, DeleteClinicStation, UpdateClinicStation, GetClinicStation
from test.routingslip.routingslip import CreateRoutingSlip, UpdateRoutingSlip, GetRoutingSlip, DeleteRoutingSlip, CreateRoutingSlipEntry, GetRoutingSlipEntry, UpdateRoutingSlipEntry, DeleteRoutingSlipEntry
import random

def awayWorker(mc):
    clinicstations = mc._clinicstationids 
    random.shuffle(clinicstations)
    for x in clinicstations:
        time.sleep(randint(60, 300))
        busy = True
        while busy == True:
            time.sleep(5)
            y = GetClinicStation(mc._host, mc._port, mc._token)
            y.setId(x)
            ret = y.send(timeout=30)
            if ret[0] == 200:
                if ret[1]["active"] == False:
                    break
        y = UpdateClinicStation(mc._host, mc._port, mc._token, x)
        y.setActive(False)
        awaytime = randint(1, 5)
        y.setAwayTime(awaytime)
        y.setAway(True)
        ret = y.send(timeout=30)
        if ret[0] == 200:
            time.sleep(awaytime * 60)
            y.setAway(False)
            ret = y.send(timeout=30)

def checkinWorker(clinicstationid, mockclinic):
    print("checkinWorker starting thread for clinic station {}".format(clinicstationid))
    host = mockclinic._host
    port = mockclinic._port
    token = mockclinic._token
    clinicid = mockclinic.getClinic()
    while True:
        time.sleep(randint(1, 30))
        # get queue for this clinicstation 
        # if item in queue, checkin the patient, work for some
        # random amount of time, then check out
    
        x = GetClinicStation(host, port, token)
        x.setId(clinicstationid)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            if ret[1]["away"] == True:
                continue

        x = GetQueue(host, port, token)
        x.setClinic(clinicid)
        x.setClinicStation(clinicstationid)
        ret = x.send(timeout=30)
        if ret[0] == 200 and len(ret[1]["queues"]) > 0:
            try:
                print("query queues for clinicstation {} got {}".format(clinicstationid, ret[1]))
                entries = ret[1]["queues"][0]["entries"]
                if len(entries):
                    # something in the queue
                    entry = entries[0]
                    q = DeleteQueueEntry(host, port, token)
                    q.setQueueEntryId(entry["id"])
                    ret = q.send(timeout=30)
                    if ret[0] == 200:
                        print("GetQueue: deleted queueentry {}".format(entry["id"]))
                        y = UpdateClinicStation(host, port, token, clinicstationid)
                        y.setActive(True)
                        y.setActivePatient(entry["patient"])
                        ret = y.send(timeout=30)
                        if ret[0] == 200:
                            print("GetQueue: set clinicstation {} active patient to {}".format(clinicstationid, entry["patient"]))
                            z = UpdateRoutingSlipEntry(host, port, token, entry["routingslipentry"])
                            z.setState("Checked In")
                            ret = z.send(timeout=30)
                            if ret[0] == 200:
                                print("GetQueue: clinicstation {} checked in patient {}".format(clinicstationid, entry["patient"]))
                                r = CreateStateChange(host, port, token)
                                r.setClinicStation(clinicstationid)
                                r.setPatient(entry["patient"])
                                r.setState("in")
                                ret = r.send(timeout=30)
                                if ret[0] == 200:
                                    # do some work
                                    t = randint(1, 600)
                                    print("GetQueue: clinicstation {} starting work on patient {} for {} seconds".format(clinicstationid, entry["patient"], t))
                                    time.sleep(t)
                                    z.setState("Checked Out")
                                    ret = z.send(timeout=30)
                                    if ret[0] == 200:
                                        print("GetQueue: clinicstation {} checked out patient {}".format(clinicstationid, entry["patient"]))
                                        r.setState("out")
                                        ret = r.send(timeout=30)
                                        if ret[0] == 200:
                                            y.setActive(False)
                                            ret = y.send(timeout=30)
                                            if ret[0] == 200:
                                                print("GetQueue: set clinicstation {} active state to False".format(clinicstationid))
                                            else:
                                                print("GetQueue: failed to set clinicstation active to false {}".format(ret[0]))
                                        else:
                                            print("GetQueue: failed to create statechange record for state 'out' {}".format(ret[0]))
                                    else:
                                        print("GetQueue: failed to set state to 'Checked Out' {}".format(ret[0]))
                                else:
                                    print("GetQueue: failed to create statechange record for state 'in' {}".format(ret[0]))
                            else:
                                print("GetQueue: failed to set state to 'Checked In' {}".format(ret[0]))
                        else:
                            print("GetQueue: failed to set clinicstation active patient id {} : {}".format(entry["patient"], ret[0]))
                    else: 
                        print("GetQueue: failed to delete queue entry {}  {}".format(entry["id"], ret[0]))
                else:
                    print("GetQueue: no waiting entries for clinicstation {}".format(clinicstationid))
            except Exception as e:
                msg = sys.exc_info()[0]
                print("GetQueue: exception {}: {}".format(ret[1], msg))
        else:
            print("GetQueue: failed to get queue entry for clinicstation {}: {}".format(clinicstationid, ret[0]))

class MockClinic: 
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password

        self._clinicid = None
        self._stationids = []
        self._clinicstationids = []
        self._patientids = []
        self._routingslipids = []
        self._routingslipentryids = []

        self._categories = ["New Cleft", "Dental", "Returning Cleft", "Ortho", "Other"]

    def login(self):
        retval = True

        login = Login(self._host, self._port, self._username, self._password)
        ret = login.send(timeout=30)
        if ret[0] == 200:
            self._token = ret[1]["token"]
        else:
            print("unable to login")
            retval = False
        return retval
        
    def logout(self):
        logout = Logout(self._host, self._port)
        ret = logout.send(timeout=30)

    def getPatients(self):
        return self._patientids

    def simulateCheckins(self):
        # create a thread for each station and then perform checkins, simulated
        # service for some random duration, then checkouts while there are still
        # patients waiting to be seen
        threads = []
        for x in self._clinicstationids:
            t = threading.Thread(target=checkinWorker, args=(x,self,))
            t.start()
            threads.append(t)
        return threads

    def simulateAway(self):
        t = threading.Thread(target=awayWorker, args=(self,))
        t.start()

    def getClinic(self):
        return self._clinicid

    def getStations(self):
        return self._stationids

    def getStationName(self, station):
        retval = None
        x = GetStation(self._host, self._port, self._token, station)
        ret = x.send(timeout=30)
        if ret[0] == 200:
            retval = ret[1]["name"]
        else:
            print("unable to get data for station {}".format(station))
        return retval
        
    def getQueue(self, clinicstationid):
        pass

    def createCategories(self):
        for x in self._categories:
            data = {}
            data["name"] = x
            r = CreateCategory(self._host, self._port, self._token, data)
            ret = r.send(timeout=30)
            if ret[0] != 200:
                print("failed to create category {}".format(x))

    def createClinic(self, location):
        # create clinic that is occurring today, since scheduler will only
        # process a clinic that is currently active.

        retval = None

        today = datetime.utcnow().strftime("%m/%d/%Y")
        todayplusone = (datetime.utcnow() + timedelta(hours=24)).strftime("%m/%d/%Y")
        x = CreateClinic(self._host, self._port, self._token, location, today, todayplusone)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create clinic {} {} {}".format(location, today, todayplusone))
        else:
            self._clinicid = ret[1]["id"]
            retval = self._clinicid
        return retval

    def createStation(self, name):
        retval = None
        x = CreateStation(self._host, self._port, self._token, name)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create station {}".format(name))
        else:
            self._stationids.append(int(ret[1]["id"]))
            retval = int(ret[1]["id"])
        return retval

    def createClinicStation(self, clinicid, stationid, name):
        retval = None        
        '''
        state = randint(0, 1)
        if state == 0:
            away = False
            state = randint(0, 1)
            if state == 1:
                active = True 
            else:
                active = False
        else:
            away = True
            active = False
        '''
        away = False
        active = False
        print("Creating clinicstation {} away {} active {}".format(name[0], away, active))
        x = CreateClinicStation(self._host, self._port, self._token, clinicid, stationid, name=name[0], name_es=name[1], away=away, active=active)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create clinicstation {}".format(name))
        else:
            self._clinicstationids.append(int(ret[1]["id"]))
            retval = int(ret[1]["id"])
        return retval

    def createPatient(self, data):
        retval = None
        x = CreatePatient(self._host, self._port, self._token, data)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("failed to create patient {}".format(data))
        else:
            self._patientids.append(int(ret[1]["id"]))
            retval = int(ret[1]["id"])
        return retval

    def createRoutingSlip(self, patient, clinic, category):
        retval = None
        if not patient in self._patientids:
            print("failed to create routingslip invalid patient {}".format(patient))
        elif clinic != self._clinicid:
            print("failed to create routingslip invalid clinic {}".format(clinic))
        else:
            x = CreateRoutingSlip(self._host, self._port, self._token)
            x.setClinic(clinic)
            x.setPatient(patient)
            x.setCategory(category)
            ret = x.send(timeout=30)
            if ret[0] != 200:
                print("failed to create routingslip patient {} clinic {} category {}".format(patient, clinic, category))
            else:
                self._routingslipids.append(int(ret[1]["id"]))
                retval = int(ret[1]["id"])
        return retval

    def createRoutingSlipEntry(self, routingslip, station):
        retval = None
        if not routingslip in self._routingslipids:
            print("failed to create routingslip entry invalid routingslip {}".format(routingslip))
        elif not station in self._stationids:
            print("failed to create routingslip entry invalid station {}".format(station))
        else:
            x = CreateRoutingSlipEntry(self._host, self._port, self._token)
            x.setRoutingSlip(routingslip)
            x.setStation(station)
            ret = x.send(timeout=30)
            if ret[0] != 200:
                print("failed to create routingslip entry routingslip {} station {}".format(routingslip, station))
            else:
                self._routingslipentryids.append(int(ret[1]["id"]))
                retval = int(ret[1]["id"])
        return retval

    def getRandomCategory(self):
        return self._categories[randint(0, len(self._categories)) - 1]    

    def randomBoolean(self):   
        ret = True
        x = randint(0, 1)
        if x == 0:
            ret = False
        return ret;

    def addPhoto(self, clinicid, genderStr, patientid):
        # figure out what image to use

        imageid = patientid % 10
        if genderStr == "Female":
            image = "images/girlfront-{}.jpg".format(imageid);
        else:
            image = "images/boyfront-{}.jpg".format(imageid);

        # load it, and base64 encode it

        with open(image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        x = CreateImage(self._host, self._port, self._token)
        x.setPatient(patientid)
        x.setClinic(clinicid)
        x.setType("Headshot")
        x.setData(encoded_string)  
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("Unable to create patient headshot photo clinic {} patient {} ret {}".format(clinicid, patientid, ret[0]))

    def createMedicalHistory(self, clinicid, patientid):    
        x = CreateMedicalHistory(self._host, self._port, self._token, patient=patientid, clinic=clinicid)

        data = {}
        data["cold_cough_fever"] = self.randomBoolean()
        data["hivaids"] = self.randomBoolean()
        data["anemia"] = self.randomBoolean()
        data["athsma"] = self.randomBoolean()
        data["cancer"] = self.randomBoolean()
        data["congenitalheartdefect"] = self.randomBoolean()
        data["congenitalheartdefect_workup"] = self.randomBoolean()
        data["congenitalheartdefect_planforcare"] = self.randomBoolean()
        data["diabetes"] = self.randomBoolean()
        data["epilepsy"] = self.randomBoolean()
        data["bleeding_problems"] = self.randomBoolean()
        data["hepititis"] = self.randomBoolean()
        data["tuberculosis"] = self.randomBoolean()
        data["troublespeaking"] = self.randomBoolean()
        data["troublehearing"] = self.randomBoolean()
        data["troubleeating"] = self.randomBoolean()
        data["pregnancy_duration"] = randint(6, 9)
        data["pregnancy_smoke"] = self.randomBoolean()
        data["birth_complications"] = self.randomBoolean()
        data["pregnancy_complications"] = self.randomBoolean()
        data["mother_alcohol"] = self.randomBoolean()
        data["relative_cleft"] = self.randomBoolean()
        data["parents_cleft"] = self.randomBoolean()
        data["siblings_cleft"] = self.randomBoolean()
        data["meds"] = ""
        data["allergymeds"] = ""
        data["first_crawl"] = randint(6, 9)
        data["first_sit"] = randint(6, 9)
        data["first_walk"] = randint(9, 14)
        data["first_words"] = randint(11, 15)
        data["birth_weight"] = 3
        data["birth_weight_metric"] = self.randomBoolean()
        data["height"] = 61
        data["height_metric"] = self.randomBoolean()
        data["weight"] = 9
        data["weight_metric"] = self.randomBoolean()

        x.setMedicalHistory(data)
        ret = x.send(timeout=30)
        if ret[0] != 200:
            print("Unable to set medical history clinic {} patient {} ret {}".format(clinicid, patientid, ret[0]))

    def createAllPatients(self, clinic, count):
        for i in xrange(0, count):
            data = {}
            data["paternal_last"] = "{}abcd1234".format(i)
            data["maternal_last"] = "yyyyyy"
            data["first"] = "zzzzzzz"
            data["middle"] = ""
            data["suffix"] = "Jr."
            data["prefix"] = ""
            data["dob"] = "04/01/1962"
            female = randint(0, 1)
            if female:
                data["gender"] = "Female"
            else:
                data["gender"] = "Male"
            data["street1"] = "1234 First Ave"
            data["street2"] = ""
            data["city"] = "Ensenada"
            data["colonia"] = ""
            data["state"] = u"Baja California"
            data["phone1"] = "1-111-111-1111"
            data["phone2"] = ""
            data["email"] = "patient@example.com"
            data["emergencyfullname"] = "Maria Sanchez"
            data["emergencyphone"] = "1-222-222-2222"
            data["emergencyemail"] = "maria.sanchez@example.com"
            id = self.createPatient(data)
            self.createMedicalHistory(clinic, id)
            self.addPhoto(clinic, data["gender"], id)

    def createClinicResources(self):
        print("Creating patient categories")
        self.createCategories()
        print("Creating clinic")
        clinic = self.createClinic("Ensenada")
        print("Creating stations")
        dental = self.createStation("Dental")
        ent = self.createStation("ENT")
        ortho = self.createStation("Ortho") 
        xray = self.createStation("X-Ray") 
        surgery = self.createStation("Surgery Screening") 
        speech = self.createStation("Speech") 
        audiology = self.createStation("Audiology") 

        dentalStations = []
        for x in [("Dental1","Dental1"), ("Dental2","Dental2"), ("Dental3", "Dental3"), ("Dental4","Dental4"), ("Dental5","Dental5")]:
            print("Creating station {}".format(x))
            dentalStations.append(self.createClinicStation(clinic, dental, x))
        entStation = self.createClinicStation(clinic, ent, ("ENT","Otorrinolaringología")) 
        print("Creating station {}".format("ENT"))
        orthoStations = []
        for x in [("Ortho1","Ortho1"), ("Ortho2","Ortho2")]:
            print("Creating station {}".format(x))
            orthoStations.append(self.createClinicStation(clinic, ortho, x))
        print("Creating station {}".format("X-Ray"))
        xrayStation = self.createClinicStation(clinic, xray, ("X-Ray","Radiografía")) 
        print("Creating station {}".format("Surgery Screening"))
        surgeryStation = self.createClinicStation(clinic, surgery, ("Surgery Screening","Examen de la cirugía")) 
        print("Creating station {}".format("Speech"))
        speechStation = self.createClinicStation(clinic, speech, ("Speech","Logopeda")) 
        print("Creating station {}".format("Audiology"))
        audiologyStation = self.createClinicStation(clinic, audiology, ("Audiology", "Audiólogo")) 

def usage():
    print("mockclinic [-h host] [-p port] [-u username] [-w password] [-c] [-a interval]") 

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ach:p:u:w:")
    except getopt.GetoptError as err:
        print str(err) 
        usage()
        sys.exit(2)
    host = "127.0.0.1"
    port = 8000
    username = None
    password = None
    doCheckins = False
    doAway = False
    numAway = 0
    for o, a in opts:
        if o == "-a":
            doAway = True
        elif o == "-c":
            doCheckins = True
        elif o == "-h":
            host = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            username = a
        elif o == "-w":
            password = a
        else:   
            assert False, "unhandled option"

    mock = MockClinic(host, port, username, password)   
    if mock.login():
        mock.createClinicResources()
        clinic = mock.getClinic()
        n = randint(90, 100)
        print("Registering {} patients for this clinic".format(n))
        mock.createAllPatients(clinic, n)
        checkinThreads = None
        awayThreads = None
        if doCheckins:
            checkinThreads = mock.simulateCheckins()
        if doAway:
            awayThreads = mock.simulateAway() 
        for x in mock.getPatients():
            time.sleep(randint(1, 30))
            cat = mock.getRandomCategory()
            routingslip = mock.createRoutingSlip(x, clinic, cat)
            print("\n\nCreating routingslip for {} patient {} at UTC time {}".format(cat, x, datetime.utcnow().strftime("%H:%M:%S")))
            for y in mock.getStations():
                if randint(0, 1) == 1:
                    print("Adding station {} to routing slip".format(mock.getStationName(y)))
                    mock.createRoutingSlipEntry(routingslip, y)    
        mock.logout()
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

if __name__ == "__main__":
    main()
