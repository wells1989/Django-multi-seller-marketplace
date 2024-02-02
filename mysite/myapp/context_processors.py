def user_context(request):
    return {'user': request.user}