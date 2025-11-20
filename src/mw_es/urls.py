from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    # path('election/', include('apps.election.urls')),
    path('api/election/', include('apps.election.urls'))
]
