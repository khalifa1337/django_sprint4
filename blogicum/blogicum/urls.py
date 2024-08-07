from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:homepage'),
        ),
        name='registration',
    ),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'