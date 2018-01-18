'''
unit tests for surgery history application. Assumes django server is up
and running on the specified host and port
'''

import unittest
import getopt, sys
import json

from service.serviceapi import ServiceAPI
from test.tscharts.tscharts import Login, Logout
from test.patient.patient import CreatePatient, DeletePatient
from test.surgerytype.surgerytype import CreateSurgeryType, DeleteSurgeryType

class CreateSurgeryHistory(ServiceAPI):
    def __init__(self, host, port, token):
        super(CreateSurgeryHistory, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self.setURL("tscharts/v1/surgeryhistory/")

    def setSurgeryHistory(self, history):
        for k, v in history.iteritems():
            self._payload[k] = v
        self.setPayload(self._payload)

class GetSurgeryHistory(serviceAPI):
    def makeURL(self):
        hasQArgs = False
        if not self._id == None:
            base = "tscharts/v1/surgeryhistory/{}/".format(self._id)
        else:
            base = "tscharts/v1/surgeryhistory/"

        if not self._patientid == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "patientid={}".format(self._patientid)
            hasQArgs = True

        if not self._surgeryname == None:
            if not hasQArgs:
                base += "?"
            else:
                base += "&"
            base += "surgeryname={}".format(self._surgeryname)
            hasQArgs = True

        self.setURL(base)

    def __init__(self, host, port, token):
        super(GetSurgeryHistory, self).__init__()

        self.setHttpMethod("GET")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._patientid = None
        self._surgeryname = None
        self._id = None
        self.makeURL()
   
    def setId(self, id):
        self._id = id;
        self.makeURL()
 
    def setPatient(self, patient):
        self._patientid = patient
        self.makeURL()

    def setSurgery(self, surgery):
        self._surgeryname = surgery
        self.makeURL()

class UpdateSurgeryHistory(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(UpdateSurgeryHistory, self).__init__()
        
        self.setHttpMethod("PUT")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self._payload = {}
        self.setPayload(self._payload) #patientid is fixed
        self.setURL("tscharts/v1/surgeryhistory/{}/".format(id))

    def setSurgeryHistory(self, history): #history might include: surgeryname, year, month, location, anesthesia problem(T/F), bleeding problem(T/F).
        for k, v in history.iteritems():
            self._payload[k] = v
        self.setPayload(self._payload)

class DeleteSurgeryHistory(ServiceAPI):
    def __init__(self, host, port, token, id):
        super(DeleteSurgeryHistory, self).__init__()
        
        self.setHttpMethod("DELETE")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)
        self.setURL("tscharts/v1/surgeryhistory/{}/".format(id))

class TestTSSurgeryHistory(unittest.TestCase):

    def setUp(self):
        login = Login(host, port, username, password)
        ret = login.send(timeout=30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("token" in ret[1])
        global token
        token = ret[1]["token"]

    def testCreateSurgeryHistory(self):
        data = {}     

        data["paternal_last"] = "abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
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

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        data = {}

        data["name"] = "Surgery1"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid = int(ret[1]["id"])

        x = CreateSurgeryHistory(host, port, token)
        
        data = {}
        data["patientid"] = patientid
        data["surgeryname"] = "Surgery1"
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True
        
        x.setSurgeryHistory(data)
    
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("patientid" in ret[1])
        patientId = int(ret[1]["patientid"])
        self.assertTrue(patientId == patientid)
 
        data = ret[1]
        self.assertTrue("surgeryname" in data)
        self.assertTrue("surgeryyear" in data)
        self.assertTrue("surgerymonth" in data)
        self.assertTrue("surgerylocation" in data)
        self.assertTrue("anesthesia_problems" in data)
        self.assertTrue("bleeding_problems" in data)

        self.assertTrue(data["surgeryname"] == "Surgery1")
        self.assertTrue(data["surgeryyear"] == 1999)
        self.assertTrue(data["surgerymonth"] == 12
        self.assertTrue(data["surgerylocation"] == "Place1")
        self.assertTrue(data["anesthesia_problems"] == True)
        self.assertTrue(data["bleeding_problems"] == True)

        x = GetSurgeryHistory(host, port, token)
        x.setPatient(patientid)
        x.setSurgery("Surgery1")
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("surgeryname" in ret[1])
        self.assertTrue("patientid" in ret[1])
        patientId = int(ret[1]["patientid"])
        self.assertTrue(patientId == patientid) 
       
        data = ret[1]
        self.assertTrue("surgeryname" in data)
        self.assertTrue("surgeryyear" in data)
        self.assertTrue("surgerymonth" in data)
        self.assertTrue("surgerylocation" in data)
        self.assertTrue("anesthesia_problems" in data)
        self.assertTrue("bleeding_problems" in data)

        self.assertTrue(data["surgeryname"] == "Surgery1")
        self.assertTrue(data["surgeryyear"] == 1999)
        self.assertTrue(data["surgerymonth"] == 12
        self.assertTrue(data["surgerylocation"] == "Place1")
        self.assertTrue(data["anesthesia_problems"] == True)
        self.assertTrue(data["bleeding_problems"] == True)
        
        x = DeleteSurgeryHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404) 
        
        data = {}
        data["patientid"] = 9999
        data["surgeryname"] = "Surgery1"
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        #Non-exist patient param
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)
        
        data = {}
        data["patientid"] = patientid
        data["surgeryname"] = "aaaa"
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        #Non-exist surgery
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
        
        #no data
        x = CreateSurgeryHistory(host, port, token)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
       
        #invalid data boolean argu
        data = {}
        data["patientid"] = patientid
        data["surgeryname"] = "Surgery1"
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = 123
        data["bleeding_problems"] = 1234
        
        x = CreateSurgeryHistory(host, port, token)
        x.setSurgeryHistory(data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = DeleteSurgeryType(host, port, token, surgeryid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
    
    def testDeleteSurgeryHistory(self):
        data = {}

        data["paternal_last"] = "abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
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

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        data = {}

        data["name"] = "Surgery1"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid = int(ret[1]["id"])

        x = CreateSurgeryHistory(host, port, token)

        data = {}
        data["patientid"] = patientid
        data["surgeryname"] = "Surgery1"
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = DeleteSurgeryHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)  # not found

        x = DeleteSurgeryHistory(host, port, token, 9999)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteSurgeryHistory(host, port, token, None)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeleteSurgeryHistory(host, port, token, "")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 400)

        x = DeleteSurgeryHistory(host, port, token, "Hello")
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 404)

        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

        x = DeleteSurgery(host, port, token, surgeryid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)

    def testUpdateSurgeryHistory(self):
        data = {}

        data["paternal_last"] = "abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
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

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid = int(ret[1]["id"])

        data = {}

        data["name"] = "Surgery1"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid = int(ret[1]["id"])

        x = CreateSurgeryHistory(host, port, token)

        data = {}
        data["patientid"] = patientid
        data["surgeryname"] = "Surgery1"
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("patientid" in ret[1])
        patientId = int(ret[1]["patientid"])
        self.assertTrue(patientId == patientid)
        self.assertTrue("surgeryname" in ret[1])
        surgery = ret[1]["surgeryname"]
        self.assertTrue(surgery == "Surgery1") 

        data = {}
        data["surgeryyear"] = 2000
        data["surgerymonth"] = 11
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("patientid" in ret[1])
        patientId = int(ret[1]["patientid"])
        self.assertTrue(patientid == patientId)

        data = ret[1]
        self.assertTrue("surgeryname" in data)
        self.assertTrue("surgeryyear" in data)
        self.assertTrue("surgerymonth" in data)
        self.assertTrue("surgerylocation" in data)
        self.assertTrue("anesthesia_problems" in data)
        self.assertTrue("bleeding_problems" in data)

        self.assertTrue(data["surgeryname"] == "Surgery1")
        self.assertTrue(data["surgeryyear"] == 2000)
        self.assertTrue(data["surgerymonth"] == 11)
        self.assertTrue(data["surgerylocation"] == "Place1")
        self.assertTrue(data["anesthesia_problems"] == True)
        self.assertTrue(data["bleeding_problems"] == True)
        
        data = {}
        data["surgerylocation"] = "Place2"
        data["anesthesia_problems"] = False
        data["bleeding_problems"] = False

        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

        x = GetSurgeryHistory(host, port, token)
        x.setId(id)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        self.assertTrue("patientid" in ret[1])
        patientId = int(ret[1]["patientid"])
        self.assertTrue(patientid == patientId)

        data = ret[1]
        self.assertTrue("surgeryname" in data)
        self.assertTrue("surgeryyear" in data)
        self.assertTrue("surgerymonth" in data)
        self.assertTrue("surgerylocation" in data)
        self.assertTrue("anesthesia_problems" in data)
        self.assertTrue("bleeding_problems" in data)

        self.assertTrue(data["surgeryname"] == "Surgery1")
        self.assertTrue(data["surgeryyear"] == 2000)
        self.assertTrue(data["surgerymonth"] == 11)
        self.assertTrue(data["surgerylocation"] == "Place2")
        self.assertTrue(data["anesthesia_problems"] == False)
        self.assertTrue(data["bleeding_problems"] == False)

        data = {}
        data["anesthesia_problems"] = "hello"
        
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["surgeryname"] = None
        
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["surgeryyear"] = 1900
      
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["surgeryyear"] = 2500

        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {}
        data["surgerymonth"] = 24

        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)
        
        data = {}
        data["surgeryname"] = "abc"

        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 400)

        data = {} #update nothing is fine.
        x = UpdateSurgeryHistory(host, port, token, id)
        x.setSurgeryHistory(data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
       
        x = DeleteSurgeryHistory(host, port, token, id)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        
        x = DeletePatient(host, port, token, patientid)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        
        x = DeleteSurgeryType(host, port, token, surgeryid)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)

    def testGetAllSurgeryHistories(self):
        data = {}

        data["name"] = "Surgery1"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid1 = int(ret[1]["id"])

        data = {}

        data["name"] = "Surgery2"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid2 = int(ret[1]["id"])

        data = {}

        data["name"] = "Surgery3"

        x = CreateSurgeryType(host, port, token, data)
        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        surgeryid3 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "3abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
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

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid1 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "1abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
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

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid2 = int(ret[1]["id"])

        data = {}
        data["paternal_last"] = "2abcd1234"
        data["maternal_last"] = "yyyyyy"
        data["first"] = "zzzzzzz"
        data["middle"] = ""
        data["suffix"] = "Jr."
        data["prefix"] = ""
        data["dob"] = "04/01/1962"
        data["gender"] = "Female"
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

        x = CreatePatient(host, port, token, data)
        ret = x.send(timeout=30)
        self.assertEqual(ret[0], 200)
        patientid3 = int(ret[1]["id"])

        idlist = []
        data = {}
        data["patientid"] = patientid1
        data["surgeryname"] = "Surgery1"
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)

        data = {}
        data["patientid"] = patientid1
        data["surgeryname"] = "Surgery2"
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)

        data = {}
        data["patientid"] = patientid1
        data["surgeryname"] = "Surgery3"
        data["surgeryyear"] = 1999
        data["surgerymonth"] = 12
        data["surgerylocation"] = "Place1"
        data["anesthesia_problems"] = True
        data["bleeding_problems"] = True

        x.setSurgeryHistory(data)

        ret = x.send(timeout = 30)
        self.assertEqual(ret[0], 200)
        id = int(ret[1]["id"])
        idlist.append(id)
