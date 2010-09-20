from django.conf.urls.defaults import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',
    url(r'analytics/$', 'django_mousechaser.heatmap.views.store_coordinates', name='store_coordinates'),
    url(r'analytics/heatmap/(?P<id>\d{1,6})/$', 'django_mousechaser.heatmap.views.generate_heatmap', name='generate_heatmap'),
    url(r'analytics/heatmap/overview/$', 'django_mousechaser.heatmap.views.overview_heatmaps', name='overview_heatmaps'),
    url(r'analytics/elements/(?P<id>\d{1,6})/$', 'django_mousechaser.heatmap.views.retrieve_html_elements', name='retrieve_html_elements'),
    url(r'analytics/page/(?P<id>\d{1,6})/$', 'django_mousechaser.heatmap.views.retrieve_heatmap_information', name='retrieve_heatmap_information'),
    url(r'analytics/html/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),

)
