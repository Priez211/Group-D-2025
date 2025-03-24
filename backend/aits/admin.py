from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Department)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(AcademicRegistrar)
admin.site.register(Issue)
admin.site.register(Notifications)