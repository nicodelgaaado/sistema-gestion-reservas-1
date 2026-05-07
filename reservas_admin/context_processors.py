from .views import usuario_es_administrador, usuario_es_docente


def roles_usuario(request):
    return {
        'es_docente': usuario_es_docente(request.user),
        'es_administrador': usuario_es_administrador(request.user),
    }
