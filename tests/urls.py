import debug_toolbar
from django.conf.urls import url, include

urlpatterns = [url(r"^", include(debug_toolbar.urls))]
