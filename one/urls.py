from django.urls import path
from . import views
urlpatterns = [

    path("home",views.home,name='home'),
    path('add',views.add,name='add'),
    path("register",views.register,name='register'),
    path("adduser",views.adduser,name='adduser'),
    path("pregister",views.pregister,name='pregister'),
    path("endday",views.endday,name='endday'),
    path("loaddb",views.loaddb,name='loaddb'),
    path("CAtracker",views.editrec,name='editrec'),
    path("StartOp",views.startop,name='startop'),
    path("endrun",views.endrun,name='endrun'),
    path("dash",views.dash,name="dash"),
    path("exportdata",views.exportdata,name="exportdata"),
    path("downloadexcel",views.downloadexcel,name="downloadexcel")
]