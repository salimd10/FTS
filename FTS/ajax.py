from django_ajax.decorators import ajax

@ajax
def accounts_query(request):
    if 'q' in request.GET:
        q = request.GET['q']
        accounts = Account.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q))
    else:
        accounts = Account.objects.all()
    return [{'text': account.name,
             'description': account.description,
             'value': account.id
             } for account in accounts]

# accounts/urls.py
urlpatterns = patterns('accounts.views',
    # ...
    url(r'^ajax/accounts/$', 'accounts_query', name='accounts_query')
)