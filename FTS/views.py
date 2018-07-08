from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from FTS.forms import *
from FTS.models import *
from FTS.functions import *
import datetime
from django.core.exceptions import ObjectDoesNotExist
import string
# Create your views here.

def search(request):
    query = request.POST.get('search', '')
    if query:
        qset = (
                 Q(name__icontains=query) |
                 Q(file_id__icontains=query)
                 #Q(office__icontains=query)
                )
        results= File.objects.filter(qset)
        if len(results)==0:
            message="No files with your search parameter. Please search again."
            context={"message":message,"query":query}
        else:
            context={"results":results,"query":query}
    else:
        message ="please type in a search string"

        context={"message":message,"query":query}


    template="search.html"
    return render(request,template,context)


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
                        request.session['staff_id'] = staff.id
                        staff = Staff.objects.get(id=staff.id)
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
        if len(infiles) != 0 or len(outfiles)!= 0:
            for file in infiles:
                #if file.status == 'pending':
                incoming_files.append([file.name, file.file_id])
            for file in outfiles:
                outgoing_files.append([file.name, file.file_id])
            context = {"staff": [user.first_name, user.surname], "incoming_files": incoming_files, "outgoing_files": outgoing_files,
                       "user_list": user_list,"staff_id": staff_id, 'file_id': file.file_id}  #name":files[0].name}

        else:
            context = {'msg': 'You have no files to treat'}
        return render(request, template, context)
    else:

        return HttpResponseRedirect('/')


def admin_staff(request, staff_id):
    template = "admin.html"
    if 'staff_id' in request.session and request.session['staff_id'] == int(staff_id):
        incoming_files = []
        #outgoing_files = []
        user_list = []
        file_list = []
        n=[]
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
                n.append(tfiles)

        for data in n:
            for list in file_list:
                if data.name == list[1]:
                    file_list.remove(list)

        print(file_list)
        if len(infiles) != 0 : #or len(files) != 0:
            for file in infiles:      #incoming files
                # if file.status == 'pending':
                incoming_files.append([file.name, file.file_id])
            # for file in outfiles:
            #     outgoing_files.append([file.name, file.file_id])
            context = {"staff": [user.first_name, user.surname], "incoming_files": incoming_files,

                       "user_list": user_list, "staff_id": staff_id, 'file_list': file_list}

        else:
            context = {"user_list": user_list, 'file_list': file_list,"staff_id": staff_id}
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
        print(request.POST['file_id'])
        receiver_id = request.POST['receiver']
        file_id = request.POST['file_id']
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


# def admin_send(request, staff_id):
#     template = "send.html"
#     now=datetime.datetime.now()
#     if request.method == "POST":
#         receiver_id = request.POST['receiver']
#         file_id= request.POST['files']
#         #staff = Staff.objects.get(id=staff_id)
#         file = File.objects.get(id=int(file_id))
#         FileTracker.objects.create(file_id=file.file_id,name=file.name, sender=staff_id, receiver=receiver_id, status='pending')
#         FileTracker.objects.get(sender=str(staff_id), status='received').delete()
#         log = FilesLogs.objects.create(file_id=file.file_id, name=file.name, sender=staff_id, receiver=receiver_id, status='sent')
#         log.save()
#         context = {'mssg':"File has been sent, kindly follow up on it.", 'staff_id': staff_id}
#
#         return render(request, template, context)


def logout(request):
    if 'staff_id' in request.session:
        try:
            del request.session['staff_id']
            return HttpResponseRedirect('/')
        except:
            pass
    return None
