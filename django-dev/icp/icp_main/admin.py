from icp_main.models import Person, MemberCompany, Project, Address, PhoneNumber, EmailAddress, MemberDownload, Picture, Event, ContactRequest
from django.contrib import admin

#class PersonAdmin(admin.ModelAdmin):
		
#class MemberCompanyAdmin(admin.ModelAdmin):
	
#class ProjectAdmin(admin.ModelAdmin):
	
#admin.site.register(Person, PersonAdmin)
#admin.site.register(MemberCompany, MemberCompanyAdmin)
#admin.site.register(Project, ProjectAdmin)
admin.site.register(Person)
admin.site.register(MemberCompany)
admin.site.register(Project)
admin.site.register(Address)
admin.site.register(PhoneNumber)
admin.site.register(EmailAddress)
admin.site.register(MemberDownload)
admin.site.register(Event)
admin.site.register(Picture)
admin.site.register(ContactRequest)
