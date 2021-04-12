"""todos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from todo_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),


    #auth
    path('signup/',views.usersignup,name='signup'),
    path('login/',views.userlogin,name='login'),
    path('logout/',views.userlogout,name='logout'),

    #todos
    path('user/todos/',views.alltodos,name='alltodos'),
    path('user/todos/new/',views.newtodo,name='newtodo'),
    path('user/todos/<int:id>/',views.viewtodo,name='viewtodo'),
    path('user/todos/<int:id>/delete',views.deletetodo,name='deletetodo'),
    path('user/todos/<int:id>/complete',views.completetodo,name='completetodo'),
    path('user/todos/<int:id>/incomplete',views.incompletetodo,name='incompletetodo'),
    path('user/todos/completed',views.completed,name='completed'),
]
