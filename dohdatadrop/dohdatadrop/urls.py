"""dohdatadrop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from uploader import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('upload/', views.uploader_view, name='uploader_view'),
    path('register/', views.register, name='register'),
    path('', views.audit, name='audit'),
    path('total/<int:year>/<int:month>/<int:day>/<int:age>', views.total_cases_by_age, name='total_cases_by_age'),
    path('list/<int:year>/<int:month>/<int:day>/<int:age>', views.list_cases_by_age, name='list_cases_by_age'),
    path('case/<str:case_number>', views.case_search, name='case_search'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
