"""vtx_guru URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from django.conf import settings
#from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', include('search.urls')),
    path('analyze/', include('ace.urls')),
    path('tables/', include('charts.urls')),
    path('scores', views.scores, name='scores'),
    path('IMD', views.IMD, name='IMD'),
    path('metrics', views.metrics, name='metrics'),
    path('boxplot', views.boxplot, name='boxplot'),
    path('piechart', views.piechart, name='piechart'),
    path('chan_occur', views.chan_occur, name='chan_occur'),
    path('scores_bar', views.scores_bar, name='scores_bar'),
    path('bands_bar', views.bands_bar, name='bands_bar'),
    path('freq_dist', views.freq_dist, name='freq_dist'),
    path('credits', views.credits, name='credits'),
    path('paradox', views.paradox, name='paradox'),
]
