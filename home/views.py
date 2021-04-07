import mimetypes
import os
from time import sleep

from django.core.files import File
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, FileResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.utils.encoding import smart_str

from mysite.converter import pdf2tiff
from mysite.settings.base import MEDIA_ROOT
from mysite.settings.func import slugify


def handle_uploaded_file(f):
    res = {}
    name = slugify(f.name.split('.')[0])+"."+f.name.split('.')[-1]
    # path = os.path.abspath(__file__)
    path = MEDIA_ROOT.split('\\')
    url = f'media\\{name}'
    path[-1] = url
    path = '\\'.join(path)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    res['url'] = '/' + url.replace('\\', '/')
    res['path'] = path
    res['path_tiff'] = path[0:-4] + '.tiff'
    res['file_name'] = name
    return res


def get_files(request):
    try:
        if request.method == 'POST':
            res = handle_uploaded_file(request.FILES['file'])
            return JsonResponse(res)
    except OSError as err:
        print(err)
        return HttpResponse('Ошибка')
    return HttpResponse('Фигня какая то')


def get_file_to_link(request):
    file_location = request.GET['path']
    file_name_tiff = request.GET['file_name'][0:-4] + '.tiff'
    try:
        p = pdf2tiff(file_location)
        fp = open(p, "rb")
        response = HttpResponse(fp.read())
        fp.close()
        response['Content-Disposition'] = f'attachment;  filename="{file_name_tiff}"'

        file_type = mimetypes.guess_type(p)
        if file_type is None:
            file_type = 'application/octet-stream'
        response['Content-Type'] = file_type
        response['Content-Length'] = str(os.stat(p).st_size)
        return response

    except IOError as err:
        print(err)
        return HttpResponse(err.__str__())



def del_file_to_link(request):
    try:
        sleep(1)
        os.remove(request.GET['path'])
        os.remove(request.GET['path_tiff'])
        return HttpResponse('ok')
    except OSError as err:
        print(err)
        return HttpResponse(err.__str__())
