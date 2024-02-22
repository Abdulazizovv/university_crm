from django.contrib import admin
from .models import Employee, Document, TeacherGroup, SubmitDocument, Group


admin.site.register(Employee)
admin.site.register(Document)
admin.site.register(TeacherGroup)
admin.site.register(SubmitDocument)
admin.site.register(Group)

