from organizations.models import Organization





def navBar(request):
    post_category = Organization.objects.filter(id=12)
    context = {"post_category":post_category}
    return context