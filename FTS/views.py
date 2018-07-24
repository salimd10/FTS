from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from FTS.forms import *
from FTS.models import *
from FTS.functions import *
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django_select2.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import string
# Create your views here.

def search(request):
    template = "search.html"
    search_form = SearchForm()
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search']

            qset = (
                    Q(name__icontains=query) |
                    Q(file_id__icontains=query)
                    )
            results = FilesLogs.objects.filter(qset).order_by('-date')

            for log in results:
                if log.sender!= '':
                    u=Staff.objects.get(id=int(log.sender))
                    log.sender=u.first_name + ' '+ u.surname

                else:
                    pass

                if log.receiver != '':
                    u=Staff.objects.get(id=int(log.receiver))
                    log.receiver =u.first_name + ' '+ u.surname

                else:
                    pass


            if len(results)==0:
                message="No files with your search parameter. Please search again."
                context={"message":message,"query":query,"search_form": search_form}
                return render(request, template, context)
            else:
                paginator = Paginator(results, 10)
                page = request.GET.get('page')
                try:
                    result = paginator.get_page(page)
                except PageNotAnInteger:
                    result = paginator.page(1)
                except EmptyPage:
                    result = paginator.page(paginator.num_pages)
                context = {"results": result, "query": query, "search_form": search_form,'staff_id':str(request.session['staff_id'])}
                return render(request, template, context)
        else:
            error = form.errors  #message ="please type in a search string"
            context = {"error":error, 'form':form,'staff_id':str(request.session['staff_id'])}
            return render(request, template, context)
    else:
        print("loser!loser!loser!loser!loser!loser!loser!loser!loser!loser!")
        form = SearchForm()
        return render(request, template, {"search_form": form, 'form': form,'staff_id':str(request.session['staff_id'])})




def home(request):
    template = "index.html"
    if request.method == "POST":
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            staffs = StaffLogin.objects.filter(username=username)
            if len(staffs) != 0:
                for staff in staffs:
                    if staff.password == password and staff.username == username:
                        request.session['staff_id'] = staff.staff_id
                        staff = Staff.objects.get(id=staff.staff_id)
                        if staff.admin_status:
                            url = '/admin_staff/' + str(staff.id)
                            return HttpResponseRedirect(url)
                        else:
                            url = '/staff/' + str(staff.id)
                            return HttpResponseRedirect(url)
                    else:
                        errormsg = "Your credentials are incorrect." \
                                 "please try again"
                        form = StaffLoginForm(request.POST)
                        context = {"login": form, "errors": errormsg}
                        return render(request, template,context)

            else:
                errormsg = "staff does not exist.Please kindly Register"
                form = StaffLoginForm(request.POST)
                context= {"login": form, "errors": errormsg}
                return render(request, template, context)
        else:
            errors = form.errors
            form = StaffLoginForm(request.POST)
            context = {"login": form, "errors": errors}
            return render(request, template, context)

    else:

        form = StaffLoginForm()
        context = {"login": form}
        return render(request, template, context)


def staff(request, staff_id):
    template = "staff.html"
    if 'staff_id' in request.session and request.session['staff_id'] == int(staff_id):
        incoming_files = []
        outgoing_files = []
        user_list = []
        users=Staff.objects.all()
        user = Staff.objects.get(id=staff_id)
        infiles = FileTracker.objects.filter(receiver=str(user.id), status='pending')
        outfiles = FileTracker.objects.filter(sender=str(user.id), status='received')
        for staff in users:
            if staff.id == int(staff_id):
                pass
            else:
                name = staff.first_name + ' ' + staff.surname
                user_list.append([staff.id, name])
        reciver_list_form = staff_user_form(mychoices=user_list, mywidget=Select2Widget)
        if len(infiles) != 0 or len(outfiles)!= 0:
            for file in infiles:
                sender = Staff.objects.get(id=int(file.sender))  #getting file senders name
                incoming_files.append([file.name, file.file_id, sender.first_name+' '+sender.surname])
            for file in outfiles:
                outgoing_files.append([file.name, file.file_id])
            context = {"staff": [user.first_name, user.surname], "incoming_files": incoming_files, "outgoing_files": outgoing_files,
                       "user_list": user_list,"staff_id": staff_id, 'file_id': file.file_id, 'receiver_form':reciver_list_form}  #name":files[0].name}

        else:
            context = {'msg': 'You have no files to treat'}

        return render(request, template, context)
    else:

        return HttpResponseRedirect('/')


def admin_staff(request, staff_id):
    template = "admin.html"
    search_form=SearchForm()
    user_form=admin_user_form()
    if 'staff_id' in request.session and request.session['staff_id'] == int(staff_id):
        incoming_files = []
        user_list = []
        file_list = []
        n=[]  #buffer
        users = Staff.objects.all()
        files = File.objects.all()
        user = Staff.objects.get(id=staff_id)
        infiles = FileTracker.objects.filter(receiver=str(user.id), status='pending')
        #sentfiles = FileTracker.objects.filter(sender=str(user.id), status='pending')
        tracking_files = FileTracker.objects.all()
        for staff in users:
            if staff.id == int(staff_id):
                pass
            else:
                name = staff.first_name + ' ' + staff.surname
                user_list.append([staff.id, name])
        for file in files:
            file_list.append([file.file_id, file.name])

        for tfiles in tracking_files:
            if tfiles.sender == staff_id and tfiles.status=='received':
                pass
            else:
                n.append(tfiles)  #buffer of files not in circulation

        for data in n:
            for list in file_list:
                if data.name == list[1]:
                    file_list.remove(list)

        file_form = admin_file_form(mychoices=file_list, mywidget=Select2Widget)
        if len(infiles) != 0 : #or len(files) != 0:
            for file in infiles:      #incoming files
                # if file.status == 'pending':
                sender = Staff.objects.get(id=int(file.sender))
                incoming_files.append([file.name, file.file_id,sender.first_name+' '+sender.surname])

            context = {"staff": [user.first_name, user.surname], "incoming_files": incoming_files,

                       "user_list": user_list, "staff_id": staff_id, 'file_list': file_list, "search_form": search_form,"file_form": file_form}

        else:
            context = {"user_list": user_list, 'file_list': file_list,"staff_id": staff_id, "search_form": search_form,"file_form": file_form,"user_form": user_form}
        return render(request, template, context)
    else:

        return HttpResponseRedirect('/')


def accept(request, staff_id):
    if request.method == "GET":
        file_id = request.GET.get('file_id',False)
        staff = Staff.objects.get(id=staff_id)
        if staff.admin_status:
            template = "admin_accept.html"
        else:
            template = "accept.html"
        now = datetime.datetime.now()
        #staff = Staff.objects.get(id=staff_id)
        file = FileTracker.objects.get(receiver=str(staff_id),file_id=file_id)
        FileTracker.objects.filter(receiver=str(staff_id)).update(receiver='', status='received', sender=staff_id)
        log = FilesLogs.objects.create(file_id=file.file_id, name=file.name, sender='', receiver=staff_id, status='accepted')
        log.save()
        context = {'mssg':"File has been accepted, kindly work on it within the next 24hrs", 'staff_id': staff_id}

        return render(request, template, context)


def send(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    if staff.admin_status:
        template = "admin_accept.html"
    else:
        template = "accept.html"
    now=datetime.datetime.now()
    if request.method == "POST":
        print(request.POST)
        receiver_id = request.POST['receiver']
        file_id = request.POST['file']
        if staff.admin_status:

            file = File.objects.get(file_id=file_id)
            try:
                FileTracker.objects.get(sender=str(staff_id), status='received',file_id=file_id)
                tracker = FileTracker.objects.create(file_id=file.file_id, name=file.name, sender=staff_id,
                                                     receiver=receiver_id, status='pending')
                FileTracker.objects.get(sender=str(staff_id), status='received', file_id=file_id).delete()
            except ObjectDoesNotExist:
                tracker = FileTracker.objects.create(file_id=file.file_id, name=file.name, sender=staff_id,
                                                     receiver=receiver_id, status='pending')

            log = FilesLogs.objects.create(file_id=file.file_id, name=file.name, sender=staff_id, receiver=receiver_id,
                                           status='sent')
            tracker.save()
            log.save()
        else:
            file = FileTracker.objects.get(sender=str(staff_id),file_id=file_id)
            tracker = FileTracker.objects.create(file_id=file.file_id,name=file.name, sender=staff_id, receiver=receiver_id, status='pending')
            FileTracker.objects.get(sender=str(staff_id),status='received',file_id=file_id).delete()
            log = FilesLogs.objects.create(file_id=file.file_id, name=file.name, sender=staff_id, receiver=receiver_id, status='sent')
            tracker.save()
            log.save()
        context = {'mssg':"File has been sent, kindly follow up on it.", 'staff_id': staff_id,'status': staff.admin_status}

        return render(request, template, context)

            #####################
            #admin functionality#
            #                   #
            #####################


def add_staff(request):
    template = "add_staff.html"
    if request.method == "POST":
        staff_reg_form = StaffRegForm(request.POST)
        if staff_reg_form.is_valid():
            staff_id = staff_reg_form.cleaned_data['staff_id']
            first_name = staff_reg_form.cleaned_data['first_name']
            surname = staff_reg_form.cleaned_data['surname']
            last_name = staff_reg_form.cleaned_data['last_name']
            office = staff_reg_form.cleaned_data['office']
            admin_status = staff_reg_form.cleaned_data['admin_status']

            staff = Staff(staff_id=staff_id,first_name=first_name,surname=surname,last_name=last_name,
                          admin_status=admin_status,office=office)
            staff.save()
            return HttpResponseRedirect('/admin_staff/'+str(request.session['staff_id']))
        else:
            error=staff_reg_form.errors
            context = {'staff_reg_form': staff_reg_form,'error':error, 'staff_id':str(request.session['staff_id'])}
            return render(request, template, context)
    else:
        staff_reg_form = StaffRegForm()
        context={"staff_reg_form":staff_reg_form,'staff_id':str(request.session['staff_id'])}
        return render(request,template,context)
def add_staff_login(request):
    template = "add_staff_login.html"
    if request.method == "POST":
        add_login_form = LoginDetailsForm(request.POST)
        if add_login_form.is_valid():
            username = add_login_form.cleaned_data['username']
            password1 = add_login_form.cleaned_data['password1']
            password2 = add_login_form.cleaned_data['password2']
            staff = add_login_form.cleaned_data['staff']
            if password1 == password2:
                staff_login = StaffLogin(username=username, password=password1, staff=staff)
                staff_login.save()
                return HttpResponseRedirect('/admin_staff/'+str(request.session['staff_id']))
            else:
                return HttpResponseRedirect('/')
        else:
            error = add_login_form.errors
            context = {'add_login_form': add_login_form, 'error': error}
            return render(request, template, context)
    else:
        add_login_form = LoginDetailsForm()
        context = {"add_login_form": add_login_form,"staff_id":str(request.session['staff_id'])}
        return render(request, template, context)

def rmv_staff_login(request):
    template = "rmv_staff_login.html"
    if request.method == "POST":
        rmvform = RmvLoginForm(request.POST)
        if rmvform.is_valid():
            user = rmvform.cleaned_data['user']
            for u in user:
                StaffLogin.objects.get(staff=u.id).delete()

            #staff_login = StaffLogin(username=username, password=password, staff=staff)
            #staff_login.save()
            return HttpResponseRedirect('/admin_staff/'+str(request.session['staff_id']))
        else:
            error = rmvform.errors
            context = {'rmvform': rmvform, 'error': error,'staff_id':str(request.session['staff_id'])}
            return render(request, template, context)
    else:
        rmvform = RmvLoginForm()
        context = {"rmvform": rmvform,'staff_id':str(request.session['staff_id'])}
        return render(request, template, context)

def add_file(request):
    template = "add_file.html"
    if request.method == 'POST':
        fileform= AddFileForm(request.POST)
        if fileform.is_valid():
            file_id = fileform.cleaned_data['file_id']
            file_name = fileform.cleaned_data['file_name']
            file=File(file_id=file_id, name=file_name)
            file.save()
            return HttpResponseRedirect('/admin_staff/'+str(request.session['staff_id']))
        else:
            error = fileform.errors
            context={'errors':error}
            return render(request,template,context)
    else:
        fileform=AddFileForm()
        context={'fileform':fileform,'staff_id':str(request.session['staff_id'])}
        return render(request,template,context)

def manage_logins(request):
    return render(request, "manage_logins.html", {'staff_id':str(request.session['staff_id'])})




def logout(request):
    if 'staff_id' in request.session:
        try:
            del request.session['staff_id']
            return HttpResponseRedirect('/')
        except:
            pass
    return None


