from django.contrib.auth import logout, login, authenticate,forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import groupby
import csv
import numpy as np
from scipy import stats


def home(request):
    return render(request,'home.html')
@login_required
def logout_request(request):
    logout(request)
    return redirect('login')
@login_required
def user(request):
    return render(request,'user.html')


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
    return render(request,'register.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('user')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change.html', {'form': form})


@login_required
def createform(request):
    if request.method == 'POST':
       # myformuser = models.Form_user() 
        dictionary = request.POST
        form = models.Form()
        form.title = dictionary.get('title')
        form.description  = dictionary.get('description')
        form.owner = request.user
        form.font = dictionary.get('font')
        form.color = dictionary.get('color')
        form.save()
        #myformuser.save()
        #myformuser.form = form
        #myformuser.save()
        for key, value in dictionary.items():
            lst = key.split("@")
            if len(lst) == 4:
                if lst[1] == "1":
                    question = models.Text_question()
                    question.question_number = lst[0]
                    question.question_type = 1
                    question.question = value
                    tempo = ""
                    myvar = int(lst[3])
                    if myvar == 1:
                        tempo = "email"
                    if myvar == 2:
                        tempo = "text"
                    if myvar == 3:
                        tempo = "number"
                    question.type = tempo
                    sumanth = ""
                    if lst[2] == "1":
                        sumanth = "required"
                    else:
                        sumanth = ""
                    question.is_required = sumanth
                    question.form = form 
                    question.save()
                elif lst[1] == "2":
                    question = models.Long_question()
                    question.question_number = lst[0]
                    question.question_type = 2
                    question.question = value
                    sumanth = ""
                    if lst[2] == "1":
                        sumanth = "required"
                    else:
                        sumanth = ""
                    question.is_required = sumanth
                    question.form = form 
                    question.save()
                elif lst[1] == "3":
                    question = models.Single_mcq()
                    question.question_number = lst[0]
                    question.question_type = 3
                    question.question = value
                    sumanth = ""
                    if lst[2] == "1":
                        sumanth = "required"
                    else:
                        sumanth = ""
                    question.is_required = sumanth
                    question.form = form 
                    question.save()
                elif lst[1] == "4":
                    question = models.Multi_mcq()
                    question.question_number = lst[0]
                    question.question_type = 4
                    question.question = value
                    sumanth = ""
                    if lst[2] == "1":
                        sumanth = "required"
                    else:
                        sumanth = ""
                    question.is_required = sumanth
                    question.form = form 
                    question.save()
                elif lst[1] == "5":
                    question = models.Toggle()
                    question.question_number = lst[0]
                    question.question_type = 5
                    question.question = value
                    sumanth = ""
                    if lst[2] == "1":
                        sumanth = "required"
                    else:
                        sumanth = ""
                    question.is_required = sumanth
                    question.form = form 
                    question.is_conditional = lst[3]
                    question.save()
                elif lst[1] == "6":
                    question = models.Drop_down()
                    question.question_number = lst[0]
                    question.question_type = 6
                    question.question = value
                    sumanth = ""
                    if lst[2] == "1":
                        sumanth = "required"
                    else:
                        sumanth = ""
                    question.is_required = sumanth
                    question.form = form 
                    question.save()
                elif lst[1] == "7":
                    question = models.File_upload()
                    question.question_number = lst[0]
                    question.question_type = 7
                    question.question = value
                    sumanth = ""
                    if lst[2] == "1":
                        sumanth = "required"
                    else:
                        sumanth = ""
                    question.is_required = sumanth
                    question.form = form 
                    question.save()
                elif lst[1] == "8":
                    question = models.Rating()
                    question.question_number = lst[0]
                    question.question_type = 8
                    question.question = value
                    sumanth = ""
                    if lst[2] == "1":
                        sumanth = "required"
                    else:
                        sumanth = ""
                    question.is_required = sumanth
                    question.form = form 
                    question.save()
        for key, value in dictionary.items():
            lst = key.split('@')
            if len(lst) == 3:
                if lst[1] == "3":
                    option = models.Single_mcq_option()
                    option.option = value
                    option.option_number = lst[2]
                    option.parent = models.Single_mcq.objects.filter(form = form, question_number = lst[0])[0]
                    option.save()
                elif lst[1] == "4":
                    option = models.Multi_mcq_option()
                    option.option = value
                    option.option_number = lst[2]
                    option.parent = models.Multi_mcq.objects.filter(form = form, question_number = lst[0])[0]
                    option.save()
                elif lst[1] == "7":
                    fileupload = models.File_upload.objects.filter(form = form, question_number = lst[0])[0]
                    fileupload.extension = value
                    fileupload.save()
                elif lst[1] == "6":
                    option = models.Drop_down_option()
                    option.option = value
                    option.option_number = lst[2]
                    option.parent = models.Drop_down.objects.filter(form = form, question_number = lst[0])[0]
                    option.save()
        context = {}
        return render(request, 'user.html', context)
    context = {}
    return render(request,'create_form.html', context)
@login_required
def formlist(request):
    lst = models.Form.objects.filter(owner=request.user)
    base_url=reverse('accounts')
    print(base_url)
    context = {"list": lst, "base_url":base_url }
    return render(request, 'formlist.html', context)
@login_required
def displayform(request,pk):
    myform = models.Form.objects.get(pk=pk)
    q_lst = list(models.Text_question.objects.filter(form = myform)) + list(models.Long_question.objects.filter(form = myform)) +list(models.Single_mcq.objects.filter(form = myform)) +list(models.Multi_mcq.objects.filter(form = myform)) +list(models.Toggle.objects.filter(form = myform)) + list(models.Drop_down.objects.filter(form = myform)) +list(models.Rating.objects.filter(form = myform)) +list(models.File_upload.objects.filter(form = myform))
    q_lst.sort(key=lambda x: x.question_number)
    mylist = []
    for x in q_lst:
        if isinstance(x,models.Text_question):
            mylist.append([x,[]])
        elif isinstance(x,models.Long_question):
            mylist.append([x,[]])
        elif isinstance(x,models.File_upload):
            mylist.append([x,[]])
        elif isinstance(x,models.Rating):
            mylist.append([x,[]])
        elif isinstance(x,models.Toggle):
            mylist.append([x,[]])
        elif isinstance(x,models.Single_mcq):
            temp = list(models.Single_mcq_option.objects.filter(parent = x).order_by('option_number'))
            [print(t.option) for t in temp]
            mylist.append([x,temp])
        elif isinstance(x,models.Multi_mcq):
            temp = list(models.Multi_mcq_option.objects.filter(parent = x).order_by('option_number'))
            mylist.append([x,temp])
        elif isinstance(x,models.Drop_down):
            temp = list(models.Drop_down_option.objects.filter(parent = x).order_by('option_number'))
            mylist.append([x,temp])
    return render(request,"displayform.html", {"mylist": mylist, "form": myform})


@login_required
def entercode(request):
    if request.method == 'POST':
        dictionary = request.POST
        code = dictionary.get("code")
        lst =  list(models.Form.objects.filter(id = code))
        if len(lst) == 1:
            return redirect('flist', pk = code)
        else:
            return render(request, "entercode.html", {"lst": [1]})
    else:
        return render(request, "entercode.html", {"lst":[]})
@login_required
def answerform(request, pk):
    if request.method == "POST":
        
        owner = request.user
        form1 = models.Form.objects.get(id = pk)
        # formuserlist = list(models.Form_user.objects.filter(form = form1))
        # formuser = formuserlist[0]
        # formuser.users_set.add(owner)
        # formuser.save()
        responses = request.POST
        file_responses = request.FILES
        
        for key,value in responses.items():
            lst = key.split("@")
            initial = lst[0]
            if initial == "1":
                new_res = models.Text_response()
                new_res.parent_question = models.Text_question.objects.get(pk=int(lst[1]))
                new_res.answer = str(value)
                new_res.owner = owner
                new_res.save()
            elif initial == "2":
                new_res = models.Long_response()
                new_res.parent_question = models.Long_question.objects.get(pk=int(lst[1]))
                new_res.answer = value
                new_res.owner = owner
                new_res.save()
            elif initial == "3":
                new_res = models.Single_mcq_response()
                new_res.parent_question = models.Single_mcq.objects.get(pk=int(lst[1]))
                new_res.parent_option = models.Single_mcq_option.objects.get(pk=int(value))
                new_res.owner = owner
                new_res.save()
            elif initial == "4":
                new_res = models.Multi_mcq_response()
                new_res.parent_question = models.Multi_mcq.objects.get(pk=int(lst[1]))
                new_res.parent_option = models.Multi_mcq_option.objects.get(pk=int(lst[2]))
                new_res.owner = owner
                new_res.save()
            elif initial == "5":
                new_res = models.Toggle_response()
                new_res.parent_question = models.Toggle.objects.get(pk=int(lst[1]))
                new_res.answer = int(value)
                new_res.owner = owner
                new_res.save()
            elif initial == "6":
                new_res = models.Drop_down_response()
                new_res.parent_question = models.Drop_down.objects.get(pk=int(lst[1]))
                new_res.parent_option = models.Drop_down_option.objects.get(pk=int(value))
                new_res.owner = owner
                new_res.save()
            elif initial == "8":
                new_res = models.Rating_response()
                new_res.parent_question = models.Rating.objects.get(pk=int(lst[1]))
                new_res.owner = owner
                new_res.answer = int(value)
                new_res.save()
        for name, file in request.FILES.items():
            lst = name.split('@')
            new_res = models.File_upload_response()
            new_res.file = file
            new_res.owner = owner
            parent = models.File_upload.objects.get(pk = int(lst[1]))
            new_res.parent_question = models.File_upload.objects.get(pk = int(lst[1]))
            
            ext = str(parent.extension)
            name1=str(file.name)
            lststr = name1.split('.')
            lststr = lststr[1:]
            s = '.'
            s = s.join(lststr)
            s = "."+s
            if s != ext:
                messages.error(request, "Extensions do not match!")
                return redirect('answer-form', pk=pk)

            new_res.save()
        return render(request, 'user.html',{})

    else:
        myform = models.Form.objects.get(pk=pk)
        q_lst = list(models.Text_question.objects.filter(form = myform)) + list(models.Long_question.objects.filter(form = myform)) +list(models.Single_mcq.objects.filter(form = myform)) +list(models.Multi_mcq.objects.filter(form = myform)) +list(models.Toggle.objects.filter(form = myform)) + list(models.Drop_down.objects.filter(form = myform)) +list(models.Rating.objects.filter(form = myform)) +list(models.File_upload.objects.filter(form = myform))
        q_lst.sort(key=lambda x: x.question_number)
        mylist = []
        for x in q_lst:
            if isinstance(x,models.Text_question):
                mylist.append([x,[]])
            elif isinstance(x,models.Long_question):
                mylist.append([x,[]])
            elif isinstance(x,models.File_upload):
                mylist.append([x,[]])
            elif isinstance(x,models.Rating):
                mylist.append([x,[]])
            elif isinstance(x,models.Toggle):
                mylist.append([x,[]])
            elif isinstance(x,models.Single_mcq):
                temp = list(models.Single_mcq_option.objects.filter(parent = x).order_by('option_number'))
                
                mylist.append([x,temp])
            elif isinstance(x,models.Multi_mcq):
                temp = list(models.Multi_mcq_option.objects.filter(parent = x).order_by('option_number'))
                mylist.append([x,temp])
            elif isinstance(x,models.Drop_down):
                temp = list(models.Drop_down_option.objects.filter(parent = x).order_by('option_number'))
                mylist.append([x,temp])
        return render(request,"answerform.html", {"mylist": mylist, "form": myform})
# def viewusers(request,pk):
#     form = models.Form.objects.get(pk =pk)
#     formuserlist = list(models.Form_user.objects.filter(form = form))
#     formuser = formuserlist[0]
#     users = list(formuser.users_set.all())
#     context = {"users":users, "pk":pk}
#     return render(request,'viewusers.html',context)


@login_required
def visual(request,pk):
    if request.method=='POST':
        dic=request.POST
        form =models.Form.objects.get(id=pk)
        q_no=dic.get("question_number")
        listof=list(models.Text_response.objects.filter(parent_question__question_number=q_no, parent_question__form=form,parent_question__type='number'))  
        listof=[int(x.answer) for x in listof]
        checkno=0
        if len(listof) ==0:
            checkno=0
        else:
            checkno=1
        nparray=np.array(listof)
        mean=0
        median=0
        mode=0
        mean=np.mean(nparray)
        median=np.median(nparray)
        mode=stats.mode(nparray)
        mode=mode[0]
        lst=list(models.Single_mcq_response.objects.filter(parent_question__question_number=q_no, parent_question__form=form))
        lst.extend(list(models.Multi_mcq_response.objects.filter(parent_question__question_number=q_no, parent_question__form=form)))
        lst.extend(list(models.Drop_down_response.objects.filter(parent_question__question_number=q_no, parent_question__form=form)))
        if len(lst) == 0 and checkno==0 :
            return render(request,'question.html',{"message": "Please enter a valid question number( which has a type of Single_mcq or Multi_mcq or Drop_down)"})
        else:
            lst=[x.parent_option for x in lst]
            lst=[x.option_number for x in lst]
            lst2=list(models.Single_mcq_option.objects.filter(parent__question_number=q_no, parent__form=form))
            lst2.extend(list(models.Multi_mcq_option.objects.filter(parent__question_number=q_no, parent__form=form)))
            lst2.extend(list(models.Drop_down_option.objects.filter(parent__question_number=q_no, parent__form=form)))
            lst2=[x.option_number for x in lst2]
            lst3=[[i,lst.count(i)] for i in lst2] 
            print(lst3)    
            return render(request,'visualize.html',{"lst":lst3,"mean":mean,"median":median,"mode":mode,"checkno":checkno})

    else:
        form =models.Form.objects.get(id=pk)
        return render(request,'question.html', {"message":""})


@login_required
def export(request,pk):
    form=models.Form.objects.get(pk=pk)
    if request.user == form.owner:
        form=models.Form.objects.get(id=pk)
        lst= list(models.Drop_down_response.objects.filter(parent_question__form=form))
        lst.extend(list(models.Single_mcq_response.objects.filter(parent_question__form=form)))
        lst.extend(list(models.Text_response.objects.filter(parent_question__form=form)))
        lst.extend(list(models.Long_response.objects.filter(parent_question__form=form)))
        lst.extend(list(models.Toggle_response.objects.filter(parent_question__form=form)))
        lst.extend(list(models.File_upload_response.objects.filter(parent_question__form=form)))
        lst.extend(list(models.Rating_response.objects.filter(parent_question__form=form)))
        lst.extend(list(models.Multi_mcq_response.objects.filter(parent_question__form=form)))

        lst=[[x.owner.username, x] for x in lst]
        result = [[k] +  [j[1] for j in list(v)] for k,v in groupby(sorted(lst, key=lambda x: x[0]), lambda x: x[0])]
        lst=result

        lst2=list(models.Drop_down.objects.filter(form=form))
        lst2.extend(list(models.Single_mcq.objects.filter(form=form)))
        lst2.extend(list(models.Text_question.objects.filter(form=form)))
        lst2.extend(list(models.Long_question.objects.filter(form=form)))
        lst2.extend(list(models.Toggle.objects.filter(form=form)))
        lst2.extend(list(models.File_upload.objects.filter(form=form)))
        lst2.extend(list(models.Rating.objects.filter(form=form)))
        k=list(models.File_upload.objects.filter(form=form))
        ques=len(lst2)
        result=[]

        req_ques=[]
        s=[]
        for i in range(1,ques+1):
            req_ques.append(i)
            s.append('')
        s.append('')
        useless=[x.question_number for x in k]
        req_ques=[x for x in req_ques if x not in useless]
        #print(req_ques)
        j=[]
        j=["Users"]+req_ques
        #print(j)
        result.append(j)
        #print(result)
        for x in lst:
            s=[]
            for i in range(1,ques+1):
                s.append('')
            s.append('')
            l=[]
            l.append(x[0])
            for a in x[1:]:
         #       print(a.question_type)
                if(a.question_type==1):#|a.question_type==2|a.question_type==5|a.question_type==8):
                    s[(a.parent_question).question_number]=s[(a.parent_question).question_number]+str(a.answer)+","
          #      print(result)
                if(a.question_type==2):#|a.question_type==2|a.question_type==5|a.question_type==8):
                    s[(a.parent_question).question_number]=s[(a.parent_question).question_number]+str(a.answer)+","
                if(a.question_type==5):#|a.question_type==2|a.question_type==5|a.question_type==8):
                    s[(a.parent_question).question_number]=s[(a.parent_question).question_number]+str(a.answer)+","
                if(a.question_type==8):#|a.question_type==2|a.question_type==5|a.question_type==8):
                    s[(a.parent_question).question_number]=s[(a.parent_question).question_number]+str(a.answer)+","
          #       
                if(a.question_type==3):#|a.question_type==4|a.question_type==6):
            #        print("hello")
           #         print((a.parent_option).option_number)
                    s[(a.parent_question).question_number]=s[(a.parent_question).question_number]+str((a.parent_option).option_number)+","
                if(a.question_type==4):#|a.question_type==4|a.question_type==6):
            #        print("hello")
           #         print((a.parent_option).option_number)
                    s[(a.parent_question).question_number]=s[(a.parent_question).question_number]+str((a.parent_option).option_number)+","
                if(a.question_type==6):#|a.question_type==4|a.question_type==6):
            #        print("hello")
           #         print((a.parent_option).option_number)
                    s[(a.parent_question).question_number]=s[(a.parent_question).question_number]+str((a.parent_option).option_number)+"," 

        #    print(s[1])
            for i in req_ques:
                l.append(s[i])
        #    print(l)        
            result.append(l)    
         #   print(result)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="survey.csv"'
        writer = csv.writer(response)
        for row in result: 
            writer.writerow(row)
        return response
    else:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="survey.csv"'
        writer = csv.writer(response)
        for row in [["Your have no ownership over the requested form or there is no such form"]]: 
            writer.writerow(row)
        return response
