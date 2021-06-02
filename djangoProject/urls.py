
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('product.urls', namespace='product')),
    path('admin/', admin.site.urls),

]
