from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Post.urls')),
    path('captcha/', include('captcha.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')) ,
    # url(r'^ckeditor/', include('ckeditor_uploader.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^photo/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]