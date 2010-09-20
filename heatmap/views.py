from django_mousechaser.heatmap.models import HeatMap, Element, Page

from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.views.generic.list_detail import object_list
from django.db import transaction

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import cm as cm
from matplotlib import mlab as mlab
from matplotlib.backends.backend_agg import FigureCanvasAgg

import numpy as np
import os
from multiprocessing import Process

PAGE = ['url', 'doc_width', 'doc_height']
PROPERTIES = ['time_entered', 'time_left', 'width', 'height', 'x', 'y']

def clean_value(value):
    value = value.replace('u', '')
    value = value.replace("'", '')
    return value

def generate_screenshot(url):
    '''BUG: webkit2png does not seem to be able to interact with the Django built-in web server, it generates a time out error'''
    
    url = 'http://google.com' #Temp workaround to generate charts
    location = os.getcwd() + '/heatmap/html/images/%s.png' % url
    os.system(os.getcwd() + '/heatmap/webkit2png.py -F -o %s %s' % (location, url))
    return url.replace('/', '').replace(':', '').replace('http', '').replace('.', '')

@transaction.commit_manually
def save_coordinates(elements):
    for element in elements:
        elem = Element()
        element = elements[element]
        keys = element.keys()
        for key in keys:
            setattr(elem, key, element[key])
        elem.url = page
        elem.time_spent = elem.time_left - elem.time_entered
        del elem.time_left
        del elem.time_entered
        elem.save()
    transaction.commit()
    

def parse_coordinates(raw_data):
    x, y = [], []
    page = {}
    elements = {}
    for key, value in raw_data.iteritems():
        #print key, value
            
        if key == 'url':
            value = clean_value(value)
        else:
            value = clean_value(value)
        #print key, value
        if key.startswith('x'):
            x.append(int(value))
        elif key.startswith('y'):
            y.append(int(value))
        elif key.endswith('id'):
            print key, value
            if value not in elements:
                elements[int(value)] = {}
        elif key in PAGE:
            print key, value
            page[key] = value
        
    keys = elements.keys()
    for key in keys:
        for property in PROPERTIES:
            value = raw_data[str(key) + property]
            #print property, value
            value = clean_value(value)
            elements[key][property] = int(value)
            
    #print x, y
    #print page
    #print elements   
            
    return x, y, page, elements

def to_json(queryset):
    json_serializer = serializers.get_serializer("json")()
    return json_serializer.serialize(queryset, ensure_ascii=False)
        

def retrieve_heatmap_information(request, id):
    page = HeatMap.objects.filter(id=id)
    data = to_json(page)
    return HttpResponse(data, mimetype='application/json')
    

def retrieve_html_elements(request, id):
    elements = Element.objects.filter(url=id)
    data = to_json(elements)
    return HttpResponse(data, mimetype='application/json')
    
def overview_heatmaps(request):
    heatmaps = HeatMap.objects.all()
    return object_list(request, heatmaps, paginate_by=15, page=1, allow_empty=True, template_name='list.html')

def process_coordinates(post):
    heatmap = HeatMap()
    x, y, doc, elements = parse_coordinates(post)
    url = doc['url']
    width = doc['doc_width']
    height = doc['doc_height']
    page, created = Page.objects.get_or_create(url=url, defaults={'url':url, 'width':width, 'height':height})
    if created:
        page.save()
    heatmap.url = page
    heatmap.x_coord = x
    heatmap.y_coord = y
        
    '''
    Screenshot generator is causing a lot of trouble, commenting it out for the time
    '''
    #file = generate_screenshot(page.url)
    #heatmap.file = file
    
    heatmap.file = ''
        
    try:
        heatmap.save()
        save_coordinates(elements)
    except:
        return HttpResponseServerError()
        


def store_coordinates(request):
    if request.POST:
        process_coordinates(request.POST)
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=200)

def generate_heatmap(request, id):
    heatmap = get_object_or_404(HeatMap, pk=id)
    dpi = 150
    width = heatmap.url.width / dpi
    height = heatmap.url.height / dpi 
    gridsize = 30
    x = heatmap.x_coord[1:-1]

    x = x.replace('u', '')
    x = x.replace("'", '')
    x = x.split(',')
    x = [int(i) for i in x]

    y = heatmap.y_coord[1:-1]
    y = y.replace('u', '')
    y = y.replace("'", '')
    y = y.split(',')
    y = [int(i) for i in y]
    
    X, Y = np.meshgrid(x, y)
    x = X.ravel()
    y = Y.ravel()

    
    fig = plt.figure(figsize=(width, height), dpi=dpi, facecolor='w', edgecolor='k')
    
    #ax = fig.add_subplot(111, frame_on=False, alpha=0.5)
    rect = [0, 0,1, 1]
    ax = fig.add_axes(rect, frameon=False)
    fig.patch.set_alpha(0.3)
    ax.patch.set_alpha(0.3)
    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])
    
    ax.hexbin(x, y, C=None, gridsize=gridsize, cmap=cm.jet, bins=None, alpha=0.5)
    ax.axis([x.min(), x.max(), y.min(), y.max()])
    ax.invert_yaxis()
    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.close(fig)
    return response