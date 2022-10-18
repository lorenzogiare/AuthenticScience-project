from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newspaper.urls')), 
]

'''Django will now redirect everything
 that comes into 'http://127.0.0.1:8000/' to blog.urls 
 and looks for further instructions there.'''

