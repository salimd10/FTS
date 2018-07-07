from FTS.models import *
#import urllib2

def AddStaff(name,address,phone,email,staffid,status):
    staff= Staff.objects.create(name=name,address=address,phone=phone,email=email,StaffId=staffid,status=status)
    return staff

def AddFile(cname,cid,cunit,department):
    course = File.objects.create(CourseId=cid,CourseName=cname,CourseUnit=cunit)
    course.department=department
    return course



def AddStaffAcount(staffid,staff):
    account=StaffLogin.objects.create(username=staffid,password="staff",staff=staff)
    return account



# def SendSms(key,to,message,sender):  #message and sender must be url encoded
#     url_smstube ='http://smstube.ng/api/sms/send?key=' + key + "&to=" + to + "&text=" + message +"&from=" + sender
#     url_smart='http://api.smartsmssolutions.com/smsapi.php?username=haidaraccess@gmail.com&password=lambogini&sender=' + sender +'&recipient=' + to +'&message='+ message
#     url_bbn='https://www.bbnplace.com/sms/bulksms/bulksms.php?username=netgigs101@gmail.com&password=fibinaci&sender='+sender+'&message='+message+'&mobile='+to
#     try:
#         request=urllib2.Request(url_bbn)
#         response=urllib2.urlopen(request)
#         html=response.read()
#         return html
#
#     except IOError:
#         errmsg='Connection could not be established with server.Please try again later.'
#         return errmsg


