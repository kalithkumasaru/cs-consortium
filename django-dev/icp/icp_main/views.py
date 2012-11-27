from django.template import Context, loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from icp_main.models import MemberCompany, Project, Person, EmailAddress, PhoneNumber, Address, MemberDownload, Event, ContactRequest
from random import choice
import string
import os
import datetime
# Create your views here.

# This function populates a context with variables that should be common to all page requests
def populate_context(request, context):
	context["authenticated"] = (request.user.is_authenticated() and request.user.is_active)
	context["username"] = request.user.username
	context["is_admin"] = request.user.is_staff
	return context
	
def index(request):
	t = loader.get_template('icp_main/index.html')
#	c = Context({"username": "asdf", "authenticated" : False})
	c = Context()
	c = populate_context(request, c)
	return HttpResponse(t.render(c))

def research(request):
	t = loader.get_template('icp_main/research.html')
        c = Context()
        c = populate_context(request, c)
	return HttpResponse(t.render(c))

def showcase(request):
	projects = Project.objects.all()
	events = Event.objects.all()
	t = loader.get_template('icp_main/showcase.html')
        c = Context({"proj_list":projects, "event_list":events})
        c = populate_context(request, c)
	return HttpResponse(t.render(c))

#def showcase_by_id(request, projectid):
#	project = Project.objects.get(pk=projectid)
#	projects = Project.objects.all()
#	displayimage = project.pictures.all()[0].picture
#	t = loader.get_template('icp_main/showcase_item.html')
#       c = Context({"displayproject": project, "projectlist":projects, "displayimage": displayimage})
#       c = populate_context(request, c)
#	return HttpResponse(t.render(c))

def showcase_project(request, project_name):
	project = Project.objects.get(shortname=project_name)
	displayimage = project.pictures.all()[0].picture
	t = loader.get_template('icp_main/showcase_project.html')
        c = Context({"display": project, "displayimage": displayimage})
        c = populate_context(request, c)
	return HttpResponse(t.render(c))

def showcase_event(request, event_name):
	event = Event.objects.get(shortname=event_name)	
	displayimage = event.pictures.all()[0].picture
	downloads = event.downloads.all()
	t = loader.get_template('icp_main/showcase_event.html')
        c = Context({"display": event, "displayimage": displayimage, "downloads": downloads})
        c = populate_context(request, c)
	return HttpResponse(t.render(c))

def resource(request):
	downloads = MemberDownload.objects.all()
	t = loader.get_template('icp_main/resource.html')
        c = Context({"downloads":downloads})
        c = populate_context(request, c)
	return HttpResponse(t.render(c))

def partner(request):
	#get the company list
	companies = MemberCompany.objects.all()
	t = loader.get_template('icp_main/partner.html')
        c = Context({"companies": companies})
        c = populate_context(request, c)
	return HttpResponse(t.render(c))

def contact(request):
	#get all of the NDSU people listed as a contact
	ndsupeople = Person.objects.filter(company="NDSU")
	ndsucontacts = ndsupeople.filter(is_company_contact=True)
	contactpeople = list()
	for person in ndsucontacts:
		emails = EmailAddress.objects.filter(name=person.name)
		phones = PhoneNumber.objects.filter(name=person.name)
		address = Address.objects.filter(person__name__iexact=person.name)
		emaillist = list()
		phonelist = list()
		personinfo = dict()
#		for emailaddress in emails:
#			emaillist.append(emailaddress)
#		for phonenumber in phones:
#			phonelist.append(phones)
		personinfo["emails"] = emails
		personinfo["phones"] = phones
		personinfo["address"] = address
		personinfo["person"] = person
		contactpeople.append(personinfo)

	c = Context({"contactlist":contactpeople})
	c = populate_context(request, c)

	if request.method == "POST":
		#save the contact to the 'contacts' list
		conRequest = ContactRequest()
		conRequest.name = request.POST['realname']
		conRequest.company = request.POST['company']
		conRequest.position = request.POST['position']
		conRequest.email = request.POST['email']
		conRequest.interest = request.POST['comments']
		conRequest.time = datetime.datetime.now()
		#email the NDSU contacts
		send_mail('ICP contact request', 'Company: ' + conRequest.company + '\nName: ' + conRequest.name + '\nEmail: ' + conRequest.email + '\nPosition: ' + conRequest.position + '\nTime submitted: ' + conRequest.time.isoformat() + '\nMessage: ' + conRequest.interest , 'no_reply@cs.ndsu.nodak.edu', ['adam.helsene@ndsu.edu'], fail_silently=False)
		t = loader.get_template('icp_main/contact_submitted.html')
		c['submit_message'] = 'Thank you for you interest in the NDSU Industry Consortium Program. A representative will contact you regarding the ICP soon.'	
		conRequest.save()
	else:
		t = loader.get_template('icp_main/contact.html')

	return HttpResponse(t.render(c))

def loginpage(request):
	username = request.POST['name']
	password = request.POST['pass']
	referer = request.META['HTTP_REFERER']
	user = authenticate(username=username, password=password)
	auth = False
	if user is not None:
        	if user.is_active:
         	   	login(request, user)
			message = "success"
			auth = True
        	else:
			message = "inactive"	
			auth = False
	else:
		message = "failed"
		auth = False
	t = loader.get_template('icp_main/login.html')
	c = Context({"authenticated": auth, "message": message, "referer": referer})
        c = populate_context(request, c)
	return HttpResponse(t.render(c))
	
	
def logoutpage(request):
	logout(request)
	t = loader.get_template('icp_main/logout.html')
	c = Context()
	c = populate_context(request, c)
	return HttpResponse(t.render(c))

# secure the crap out of this plox... kthnx...
def memberdownload(request, filename):
	if (request.user.is_authenticated() and request.user.is_active):
		# WARNING: THE FOLLOWING PATH NEEDS TO BE CHANGED WHEN 
		#	PROMOTED TO PRODUCTION
		path_filename = '/var/django-dev/memberfiles/' + filename
		response = HttpResponse(mimetype='application/force-download')
		response['Content-Disposition']='attachment;filename="%s"'%filename
		response["X-Sendfile"] = path_filename
		response['Content-length'] = os.stat(path_filename).st_size
		return response
	return -1
		
# registers a new user. This NEEDS exception handling BADLY
def register(request):
	t = loader.get_template('icp_main/register.html')
	c = Context()
	c = populate_context(request, c)

	if request.method == "POST":
		username = request.POST.get('name')
		email = request.POST.get('mail')
		firstname = request.POST.get('profile_first_name')
		lastname = request.POST.get('profile_last_name')
		organization = request.POST.get('profile_organization')
	
		# generate password
		password = random_password()
		# create the user
		user = User.objects.create_user(username, email, password)
		user.first_name = firstname
		user.last_name = lastname
		user.save()
		#	set organization here

		# send email with confirmation
		send_mail('New account created for ICP website', 'Thank you for creating an account at the NDSU ICP website.\nYour account will allow us to contact you regarding the Consortium as well as allow you to access Consortium member-specific resources if your company is a member.\n\n\tYour username is:\t'+username+'\n\tYour password has been set to:\t'+password, 'no_reply@icp.cs.ndsu.nodak.edu', [email], fail_silently=False)
		c['registered'] = True
	
	return HttpResponse(t.render(c))

def newpass(request):
	t = loader.get_template('icp_main/newpass.html')
	c = Context()
	c = populate_context(request, c)
	# on POST, grab email address, reset password, email
	if request.method == "POST":
		name = request.POST.get('user name')
		passwd = random_password()	
		# generate a new password and save it
		# try to get the entered user
		try:
			user = User.objects.get(username=name)
		except User.DoesNotExist:
			# if the user doesn't exist, set the error flag and render the page
			c['error'] = True
			return HttpResponse(t.render(c))
		user.set_password(''+passwd)
		user.save()
		email = user.email
		# email the password
		send_mail('Password reset for ICP website', 'Your password has been reset to '+passwd+' for '+name+' at the ICP website at http://icp.cs.ndsu.nodak.edu', 'password_reset@icp.cs.ndsu.nodak.edu', [email], fail_silently=False)
		c['passwordreset'] = True
		c['name'] = name
		c['email'] = email
	# on GET, do nothing fancy
		
	return HttpResponse(t.render(c))

def random_password():
	chars = string.letters + string.digits
	passwd = ''
	for i in range(8):
		passwd = passwd + choice(chars)
	return passwd

def gallery(request):
	t = loader.get_template('icp_main/all_gallery.html')
	events = Event.objects.all().order_by('-date')
	c = Context({"event_list": events})
	c = populate_context(request, c)
	return HttpResponse(t.render(c))
	
def gallery_project(request, project_name):
	project = Project.objects.get(shortname=project_name)
	pictures = project.pictures.all()
	t = loader.get_template('icp_main/gallery.html')
	c = Context({"display": project, "pictures": pictures })
	c = populate_context(request, c)
	return HttpResponse(t.render(c))

def gallery_event(request, event_name):
	event = Event.objects.get(shortname=event_name)	
	pictures = event.pictures.all()
	t = loader.get_template('icp_main/gallery.html')
	c = Context({"display": event, "pictures": pictures })
	c = populate_context(request, c)
	return HttpResponse(t.render(c))
