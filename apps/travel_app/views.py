from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Travel

# Create your views here.
def index(request):
    return redirect(main)

def main(request):

    return render(request, "main.html")

def register(request):
    check = User.objects.register(request.POST)
    print(check)
    if check["is_valid"]:
        request.session["errors"] = {}
        request.session['uid'] = check['user'].id
        return redirect(dashboard)
    else:
        request.session["errors"] = check["errors"]
        return redirect(main)

def login(request):
    check = User.objects.login(request.POST)
    if check["is_valid"]:
        request.session["errors"] = {}
        request.session['uid'] = check['user'].id
        return redirect(dashboard)
    else:
        request.session["errors"] = check["errors"]
        return redirect(main)

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'uid' not in request.session:
        return redirect('/')
    all_travel = Travel.objects.all()
    joined = User.objects.get(id=request.session['uid']).joined.all()
    others = all_travel.difference(joined)
    user = User.objects.get(id=request.session['uid'])
    context= {
        'user': user,
        'joined':joined,
        'others':others
    }
    
    return render(request, 'dashboard.html', context)

def new(request):
    user = User.objects.get(id=request.session['uid'])
    context= {
        'user': user
    }
    return render(request, 'new.html', context)

def create(request):
    check = Travel.objects.add(request.POST, request.session['uid'])
    if type(check) == list:
        for error in check:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/travel/new')

    else:
        check.joined.add(User.objects.get(id=request.session['uid']))
        return redirect('/travels')

def remove(request, id):
    trip = Travel.objects.get(id=id)
    if trip.poster.id == request.session['uid']:
        trip.delete()
    return redirect('/travels')

def view_trip(request, id):
    trip = Travel.objects.get(id=id)
    context= {
        'trip': trip
    }
    return render(request, 'view.html', context)

def join(request, id):
    trip = Travel.objects.get(id=id)
    trip.joined.add(User.objects.get(id=request.session['uid']))
    return redirect('/travels')

def unjoin(request, id):
    trip = Travel.objects.get(id=id)
    trip.joined.remove(User.objects.get(id=request.session['uid']))
    return redirect('/travels')