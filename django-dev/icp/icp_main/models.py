from django.db import models
from django.core.files.storage import FileSystemStorage


member_storage = FileSystemStorage(location='/var/django-dev/memberfiles/', base_url='/memberfiles/')

# Create your models here.
class Picture(models.Model):
	def __unicode__(self):
		return self.name
	name = models.CharField(max_length=100)
	description = models.TextField()
	picture = models.ImageField(upload_to="pictures")
	thumbnail = models.ImageField(upload_to="pictures/thumbnails")


class MemberCompany(models.Model):
	def self_unicode_filename(instance, filename):
		return 'company/' + instance.__unicode__() + '/' + filename
	companyName = models.CharField(max_length=50)
	companyDescription = models.TextField()	
	companyLogo = models.ImageField(upload_to=self_unicode_filename)
	companyURL = models.CharField(max_length=200)
	def __unicode__(self):
		return self.companyName

	

class Person(models.Model):
	company = models.ForeignKey('MemberCompany', to_field='companyName')
	name = models.CharField(max_length=50)
	is_company_contact = models.BooleanField()
	def __unicode__(self):
		return self.name

class Address(models.Model):
	person = models.ForeignKey('Person', to_field='name')
	address = models.CharField(max_length=500)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	zip = models.CharField(max_length=15)
	def __unicode__(self):
		return self.person.name

class PhoneNumber(models.Model):
	name = models.ForeignKey('Person', to_field='name')
	phone_number = models.CharField(max_length=15)
	def __unicode__(self):
		return self.phone_number

class EmailAddress(models.Model):
	name = models.ForeignKey('Person', to_field='name')
	email_address = models.CharField(max_length=200)
	def __unicode__(self):
		return self.email_address



class MemberDownload(models.Model):
#	def self_filename(instance, filename):
#		return '/var/django/memberfiles' + '/' + filename
	def __unicode__(self):
		return self.shortname
	description = models.CharField(max_length=150)
	shortname = models.CharField(max_length=30)
	file = models.FileField(upload_to="files", storage=member_storage)

class Descriptors(models.Model):
	def __unicode__(self):
		return self.name
	name = models.CharField(max_length=200)
	shortname = models.SlugField(max_length=30)
	description = models.TextField()
		
	class Meta: 
		abstract = True

class Media(models.Model):
	pictures = models.ManyToManyField(Picture, blank=True)
	downloads = models.ManyToManyField(MemberDownload, blank=True)

	class Meta:
		abstract = True

class Event(Descriptors, Media):
	def self_unicode_filename(instance, filename):
		return 'event' + '/' + instance.__unicode__() + '/' + filename
	date = models.DateField()
#	def __unicode__(self):
#		return self.name
#	name = models.CharField(max_length=100)
#	shortname = models.CharField(max_length=30)
#	descrption = models.CharField(max_length=500)
	#picture = models.ImageField(upload_to=self_unicode_filename, blank=True)
#	picture = models.ManyToManyField(Picture, blank=True)
#	downloads = models.ManyToManyField(MemberDownload, blank=True)

class Project(Descriptors, Media):
	def self_unicode_filename(instance, filename):
		return 'project' + '/' +  instance.__unicode__() + '/' + filename
	sponsors = models.ManyToManyField("MemberCompany", blank=True)
	teamMembers = models.ManyToManyField("Person", blank=True)
#	name = models.CharField(max_length=100)
	#shortname is to be used for URLS and short references
#	shortname = models.CharField(max_length=30)
#	description = models.CharField(max_length=500)
	#picture = models.ImageField(upload_to=self_unicode_filename, blank=True)
#	picture = models.ManyToManyField(Picture, blank=True)
#	def __unicode__(self):
#		return self.name

class ContactRequest(models.Model):
	
	name = models.CharField(max_length=255)
	company = models.CharField(max_length=255)
	position = models.CharField(max_length=255, blank=True)
	email = models.CharField(max_length=255)
	interest = models.CharField(max_length=1024, blank=True)
	time = models.DateTimeField()
	def __unicode__(self):
		return self.name + " - " + self.time.isoformat()

	


