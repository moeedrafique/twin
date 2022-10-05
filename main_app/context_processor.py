from organizations.models import Organization





def navBar(request):
    post_category = Organization.objects.filter(users=request.user)
    context = {"post_category":post_category}
    return context