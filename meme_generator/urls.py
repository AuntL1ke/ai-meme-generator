from django.contrib import admin
from django.urls import path
from memes import views  # 👈 імпортуй з нового app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index")
]
