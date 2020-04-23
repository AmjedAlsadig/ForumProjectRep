from django.shortcuts import render
from accounts.models import UserProfile

# Create your views here.
def searchView(request):
    query = request.GET.get('q')
    print(query)
    if query:
        try :
            users_query_list = UserProfile.objects.filter(username__icontains=query)
        except UserProfile.DoesNotExist :
            users_query_list = None
    else:
        try :
            users_query_list = UserProfile.objects.all()
        except UserProfile.DoesNotExist :
            query = None
    context = {
        'query' : query,
        'users_query_list' : users_query_list
    }
    return render(request, 'search/view.html', context)