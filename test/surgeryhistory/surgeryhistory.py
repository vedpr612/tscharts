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
    def __init__(self, host, port, token, patient):
        super(CreateSurgeryHistory, self).__init__()
        
        self.setHttpMethod("POST")
        self.setHost(host)
        self.setPort(port)
        self.setToken(token)

        self._payload = {"patientid":patient}
        self.setPayload(self._payload)
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
        self.setPayload(self._payload)
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

        x = CreateSurgeryHistory(host, port, token, patient = patientid)
        
        data = {}
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
