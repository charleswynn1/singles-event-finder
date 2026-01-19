from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SearchHistory

@login_required
def view_search_history(request):
    searches = SearchHistory.objects.filter(user=request.user)
    return render(request, 'search_history/search_history.html', {'searches': searches})