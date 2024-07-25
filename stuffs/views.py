from django.shortcuts import render, get_object_or_404
from stuffs.models import Unit
from django.contrib.admin.models import LogEntry

# Create your views here.
def dashboard(request):
    units = Unit.objects.all()
    admin_logs = LogEntry.objects.all()
    for log in admin_logs:
        print(log)
        print('by: ',log.user)
    context = {
        "title": "list of units",
        'units': units,
        'logs': admin_logs
    }
    return render(request, 'dashboard.html', context)

def unit_page(request):
    units = Unit.objects.all()
    context = {
        "title": "list of units",
        'units': units
    }
    return render(request, 'unit_page.html', context)

def unit_details(request, unit_id):
    instance = get_object_or_404(Unit, id=unit_id)
    history = instance.history.all()
    for h in history:
        print(dir(h))
    context = {
        "title": "unit details",
        'instance': instance,
        'history': history
    }
    return render(request, 'unit_detailed_page.html', context)