import os

import dicttoxml
from django.shortcuts import render
from django.views.decorators.http import require_http_methods 
from django.http import HttpResponse
from django.conf import settings

from . import recog


SAVE_DIR = os.path.join(settings.BASE_DIR, 'upload') 

@require_http_methods(['GET', 'POST']) 
def index(request): 
    if request.method == 'GET': 
        return render(request, 'index.html')

    if request.method == 'POST':
        file = request.FILES['file']

        if not os.path.exists(SAVE_DIR): 
            os.makedirs(SAVE_DIR)

        save_path = os.path.join(SAVE_DIR, file.name)

        with open(save_path, 'wb') as f: 
            f.write(file.read())

        predict = recog.recog_video(save_path)

        return render(request, 'index.html', {
            'predict': dicttoxml.dicttoxml({'seats': predict})
        })
    
