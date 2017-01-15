#!/usr/bin/python

import os
import sys
import json
import warnings
import argparse

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
from dejavu.recognize import MicrophoneRecognizer
from argparse import RawTextHelpFormatter
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
warnings.filterwarnings("ignore")
dir = os.path.dirname(__file__)
DEFAULT_CONFIG_FILE = os.path.join(dir, 'dejavu.cnf')


def init(configpath):
    try:
        with open(configpath) as f:
            config = json.load(f)
    except IOError as err:
        print("Cannot open configuration: %s. Exiting" % (str(err)))
        sys.exit(1)
    return Dejavu(config)


def index(request):
    djv = init(DEFAULT_CONFIG_FILE)
    song = djv.recognize(FileRecognizer, os.path.join(dir, 'mp3/Brad-Sucks--Total-Breakdown.mp3'))
    print "From file we recognized: %s\n" % song
    return HttpResponse("From file we recognized: %s\n" % song)

@csrf_exempt
def simple_upload(request):
    if request.method == 'POST' and request.FILES['song']:
        myfile = request.FILES['song']
        fs = FileSystemStorage()
        filename = fs.save('music_recognizer/queue/'+myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        djv = init(DEFAULT_CONFIG_FILE)
        song = djv.recognize(FileRecognizer, os.path.join(dir, 'queue/'+myfile.name))
        print "From file we recognized: %s\n" % song
        os.remove(os.path.join(dir, 'queue/'+myfile.name))
        return JsonResponse(song)
    return render(request, 'core/simple_upload.html')