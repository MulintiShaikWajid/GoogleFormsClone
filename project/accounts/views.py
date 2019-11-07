from django.contrib.auth import logout, login, authenticate,forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
import csv,sqlite3
from django.http import HttpResponse
from django.contrib.auth.models import User
def home(request):
    return render(request,'accounts/home.html')

def logout_request(request):
    logout(request)
    return redirect('login')

def user(request):
    return render(request,'accounts/user.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request,'accounts/register.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('user')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change.html', {'form': form})

def export(request):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    res = HttpResponse(content_type='text/csv')
    if request.user.is_authenticated:
        if(request.user.username == 'sumanthbalaji'):
            cur.execute("select * from accounts_Person;")
            with open ("csv1","w",newline='') as csv_file:
                res['Content-Disposition'] = 'attachment;filename="csv1.csv"'
                csv_writer = csv.writer(res)
                csv_writer.writerow([i[0] for i in cur.description])
                csv_writer.writerows(cur)
        elif(request.user.username == 'sumanth'):
            cur.execute("select * from accounts_Person2;")
            with open ("csv2","w",newline='') as csv_file:
                res['Content-Disposition'] = 'attachment;filename="csv2.csv"'
                csv_writer = csv.writer(res)
                csv_writer.writerow([i[0] for i in cur.description])
                csv_writer.writerows(cur)
    else:
        return redirect('login')
    return res


