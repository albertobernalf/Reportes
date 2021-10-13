"""reportes URL Configuration

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
from reporte01  import views as viewReport
from reporte02  import views as viewReport1

urlpatterns = [
    path('admin/', admin.site.urls),
 #  path('pdf/', viewReport.exportar_pdf),
    path('pdf/',  viewReport.nuevoPdfView.as_view()),
    path('pdf1/', viewReport1.nuevoPdfView.as_view()),
    path('pdf1/buscapaciente/<tipodoc>,<documento>', viewReport1.buscapaciente),

    path('inicio/' , viewReport1.inicioView.as_view()),
    path('grabar/<usuario>,<contrasena>', viewReport1.grabar),
    path('grabar1/<usuario>,<contrasena>,<nombre>', viewReport1.grabar1),
    path('AdmUsuarios/', viewReport1.AdmUsuariosView.as_view()),
    path('findOne/<str:usuario>,<str:contrasena>, <str:nombre>', viewReport1.Modal),

]
