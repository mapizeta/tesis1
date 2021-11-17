from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from tesis1 import settings

urlpatterns = [
    path('', views.loginView, name="homeAdmin"),
    path('perfil', views.perfil, name="perfil"),
    path('crearquiz', views.tipo_proceso, name="crearquiz"),
    path('registro', views.registro, name="registro"),
    path('accounts/login/', views.loginView, name='login'),
    path('logout_vista', views.logout_vista, name="logout_vista"),
    path('HomeUsuario', views.HomeUsuario, name="HomeUsuario"),
    path('jugar', views.jugar, name="jugar"),
    path('tablero', views.tablero, name="tablero"),
   
    path('agregarquiz', views.agregar_quiz, name="agregarquiz"),
    path('agregarrespuestas', views.agregar_respuesta, name="agregarrespuestas"),
    path('evaluados', views.evaluados, name="evaluados"),
    path('procesosasignados', views.procesosasignados, name="procesosasignados"),
    path('tablaprocesos', views.mostrar_procesos_incompletos,name="tablaprocesos"),
    path('modificarusuario/<id>', views.modificarUser,name="modificarusuario"),
    path('resultado/<int:pregunta_respondida_pk>/', views.resultado_pregunta, name="resultado"),

    path('campañas_incompletas/', views.mostrar_procesos_incompletos, name="campañas_incompletas"),
    path('preguntas/<str:proceso>/', views.mostrar_preguntas_proceso, name="preguntas_poceso"),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)