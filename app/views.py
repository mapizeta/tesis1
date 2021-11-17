#-*- encoding:utf-8 -*-
from django.contrib.auth.models import User
from django.contrib import admin
from django.http.response import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .forms import ListUser, RegistroFormulario,UsuarioLoginFormulario, preguntaquizform,respuestaquizform,tipoproceso,formcampaña,ResetPasswordForm
from django.contrib.auth import authenticate, login, logout
from .models import Proceso, QuizUsuario,Pregunta,PreguntasRespondidas, CampanaAsignada
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
# from django.core.cache import cache
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'Usuario/login.html')
@login_required
def perfil(request):
    return render(request,'perfil.html')

@login_required
def crearquiz(request):

    return render(request,'crearquiz.html')
@login_required
def tablero(request):
    total_usuarios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
    contador = total_usuarios_quiz.count()

    context = {
        'usuario_quiz':total_usuarios_quiz,
        'contar_user':contador
    }
    return render(request,'Play/tablero.html',context)
@login_required
def evaluados(request):
    total_usuarios_quiz = QuizUsuario.objects.all()
    datos_user = User.objects.all()

    context = {
        'usuario_quiz':total_usuarios_quiz,
        'datos_user':datos_user
    }
    return render(request,'Play/tablaevaluados.html',context)

def loginView(request):
    titulo='login'
    form = UsuarioLoginFormulario(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        usuario = authenticate(username=username, password=password)
        login(request, usuario)
        return redirect ('HomeUsuario')
    context = {
        'form':form,
        'titulo':titulo
    }
    return render (request, 'Usuario/login.html',context)

@login_required
def logout_vista(request):
    logout(request)
    return redirect('/')
@login_required
def HomeUsuario(request):

    return render(request, 'Usuario/homeusuario.html')
@login_required
def jugar(request):
    
    QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)


    if request.method == 'POST': 
        
        pregunta_pk = request.POST.get('pregunta_pk')
        
        pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')
        
        try:
           opcion_seleccionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
        except ObjectDoesNotExist:
                raise Http404
        QuizUser.validar_intento(pregunta_respondida,opcion_seleccionada)

        return redirect('resultado', pregunta_respondida.pk)
    
    else:
        pregunta = QuizUser.obtener_nuevas_preguntas()
        if pregunta is not None:
            QuizUser.crear_intentos(pregunta)
        context = {
            'pregunta':pregunta,
            

        }
    
    return render(request, 'Play/jugar.html' , context)
@login_required
def resultado_pregunta(request,pregunta_respondida_pk):
    respondida=get_object_or_404(PreguntasRespondidas,pk=pregunta_respondida_pk)
    context = {
        'respondida':respondida
    }
    return render(request,'Play/resultados.html',context)

    

@login_required
def registro(request):
    titulo = 'CREAR UNA CUENTA'
    mensaje = "GUARDADO CORRECTAMENTE"
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            form.save()
            mensaje()
            
    else:
        form = RegistroFormulario()
        
    context = {
        'form': form,
        'titulo': titulo

    }
    return render(request, 'Usuario/registro.html', context)
@login_required
def agregar_quiz(request):

    data = {
        'form':preguntaquizform(),
        
    }
    if request.method=='POST':
        formulario=preguntaquizform(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data['mensaje']= "guardado correctamente"

        else:
            data["form"] = formulario




    return render(request,'agregarquiz.html',data)
@login_required
def agregar_respuesta(request):
    
    data = {
        'form':respuestaquizform(),
        
    }
    if request.method=='POST':
        formulario=respuestaquizform(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('agregarrespuestas')

        else:
            data["form"] = formulario




    return render(request,'agregarrespuestas.html',data)



@login_required
def tipo_proceso(request):
    
    
    data = {
        'form':tipoproceso(data=request.POST),
        
    }
        
    
    if request.method=='POST':
        formulario=tipoproceso(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('agregarquiz')

        else:
            data["form"] = formulario




    return render(request,'crearquiz.html',data)
    
@login_required  
def procesosasignados(request):
    
    
    data = {
        'form':formcampaña(data=request.POST),
        
        
    }
        
    
    if request.method=='POST':
        formulario=formcampaña(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('HomeUsuario')

        else:
            data["form"] = formulario




    return render(request,'Procesosasignados.html',data)
    
   

@login_required
def tablaprocesos(request):
    total_procesos = CampanaAsignada.objects.all()
    campana_proceso = Proceso.objects.all()
    

    context = {
        'total_procesos':total_procesos,
        'campaña_proceso':campana_proceso
        
        
    }
    return render(request,'tablaprocesos.html',context)

@login_required
def mostrar_procesos_incompletos(request):
    from django.contrib.auth.models import User
    from django.db.models import Q
    id_usuario = User.objects.filter(username=str(request.user))
    id_usuario = id_usuario[0].id
    campanas_incompletas = CampanaAsignada.objects.filter(Q(usuarioasignado_id=id_usuario) & Q(finalizo_campana=0))
    nombre_procesos_incompletos = []
    for proceso in campanas_incompletas:
        nombre_procesos_incompletos.append(str(proceso.procesoasignado))
    context = {
        'total_procesos':len(nombre_procesos_incompletos) if len(nombre_procesos_incompletos) > 0 else 0,
        'campaña_proceso':nombre_procesos_incompletos
    }
    return render(request,'tablaprocesos.html',context)
    
def mostrar_preguntas_proceso(request,proceso):
    
    try:
        id_proceso = Proceso.objects.filter(nombreproceso=proceso)
        id_proceso = id_proceso[0].id
        preguntas = Pregunta.objects.filter(proceso_id=id_proceso)
        #se puede especificar el campo preguntas.cualquier camnpo
        #retornar con un template
        preguntas = [i.texto for i in preguntas]
        return HttpResponse(str(preguntas))

    except Exception as e:
        return HttpResponse("Ocurrio el siguiente error "+str(e))



"""
campañas incompletas va a devolver las campañas que estan incompletas por ese usario
Esas campañas(procesos) van hacer un enlace porque se va a rellenar en un contexto en un tem,pleate
Al hacer clic en un proceso se van a obtener todos las preguntas de ese proceso
"""
@login_required
def modificarUser(request,id):
    detalle = User.objects.get(id=id)
    data={
        'form':ListUser(instance = detalle)
    }

    if request.method =='POST':
        formulario =  ListUser (data=request.POST,instance=detalle)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Modificado Correctamente"
            data['form'] = formulario
            
    return render(request,'Usuario/modificarusuario.html',data)