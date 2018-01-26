# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from surgerytype.models import *
from patient.models import *
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
import sys
import numbers
import json  

class SurgeryHistoryView(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def serialize(self, entry):
        m = {}
        m["id"] = entry.id
        m["patient"] = entry.patient_id
        m["surgery"] = entry.surgery_id
        m["surgeryyear"] = entry.surgeryyear
        m["surgerymonth"] = entry.surgerymonth
        m["surgerylocation"] = entry.surgerylocation
        m["anesthesia_problems"] = entry.anesthesia_problems
        m["bleeding_problems"] = entry.bleeding_problems

        return m

    def get(self, request, surgery_history_id = None, format = None):
        surgery_history = None
        badRequest = False
        aPatient = None
        aSurgery = None
        kwargs = {}

        if surgery_history_id:
            try:
                surgery_history = SurgeryHistory.objects.get(id = surgery_history_id)
            except:
                surgery_history = None
        else:
            try:
                patientid = request.GET.get('patient','')
                if patientid != '':
                    try:
                        aPatient = Patient.objects.get(id = patientid)
                        if not aPatient:
                            badRequest = True
                        else:
                            kwargs["patient"] = aPatient
                    except:
                        badRequest = True
            except:
                pass #no patient ID

            try:
                surgeryid = request.GET.get('surgery','')
                if surgeryid != '':
                    try:
                        aSurgery = SurgeryType.objects.get(id=surgeryid)
                        if not aSurgery:
                            badRequest = True
                        else:
                            kwargs["surgery"] = aSurgery
                    except:
                        badRequest = True
           except:
               pass #no surgery ID
           if not badRequest and len(kwargs):
               case1 = False
               case2 = False
               case3 = False

               if aPatient and aSurgery:
                   case1 = True
               elif aPatient and not aSurgery:
                   case2 = True
               elif aSurgery and not aPatient:
                   case3 = True
               else:
                   badRequest = True

          
           if not badRequest:
               kwargs = {}
               if case1:
                   kwargs["patient"] = aPatient
                   kwargs["surgery"] = aSurgery
               if case2:
                   kwargs["patient"] = aPatient
               if case3:
                   kwargs["surgery"] = aSurgery
               try:
                   surgery_history = SurgeryHistory.objects.filter(**kwargs)
               except:
                   surgery_history = None

           if not surgery_history and not badRequest:
               raise NotFound
           elif not badRequest:
               if surgery_history_id:
                   ret = self.serialize(surgery_history)
               elif len(surgery_history) == 1:
                   ret = self.serialize(surgery_history[0])
               else:
                   ret = []
                   for x in surgery_history:
                       y = self.serialize(x)
                       ret.append(y)
           if badRequest:
               return HttpResponseBadRequest()
           else:
               return Response(ret)
         
