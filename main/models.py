from django.db import models



# class Education(models.Model):
#     country = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     speciality = models.CharField(max_length=255)

#     levels_choice = (
#         ("bachelor", "Bakalavr"),
#         ("magistr", "Magistr"),
#         ("phd", "Fan nomzodi(Phd)"),
#         ("dsc", "Fan doktori(Dsc)")
#     )
#     level = models.CharField(max_length=255, choices=levels_choice)
#     employee = models.ForeignKey("Employee", on_delete=models.CASCADE)


class Subject(models.Model):
    fakultet = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    hours = models.IntegerField(default=0)
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    


class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="images/", default="images/default.jpg")
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    citizenship = models.CharField(max_length=255, verbose_name="Fuqarolik")
    pass_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Passport raqami")
    pass_date = models.DateField(null=True, verbose_name="Passport muddati")
    jshshir = models.CharField(max_length=14, null=True)
    country = models.CharField(max_length=255, verbose_name="Mamlakat")
    village = models.CharField(max_length=255, null=True, blank=True, verbose_name="Viloyat")
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name="shahar/tuman")
    birth_date = models.DateField(null=True, verbose_name="Tug'ilgan kun")
    gender = models.CharField(max_length=35, verbose_name="Jinsi")
    live_village = models.CharField(max_length=255, null=True, verbose_name="Yashayotgan Viloyati")
    live_city = models.CharField(max_length=255, null=True, verbose_name="Yashayotgan shahar/tumani")
    live_mfy = models.CharField(max_length=255, null=True, verbose_name="Yashayotgan MFY")
    live_street = models.CharField(max_length=255, null=True, verbose_name="Ko'cha")
    live_home = models.CharField(max_length=255, null=True, verbose_name="uy")

    edu_country = models.CharField(max_length=255, null=True, blank=True)
    edu_name = models.CharField(max_length=255, null=True, blank=True)
    speciality = models.CharField(max_length=255, null=True, blank=True)
    edu_degree = models.CharField(max_length=255, null=True, blank=True)


    status_choices = (
        ("active", "active"),
        ("inactive", "inactive")
    )
    status = models.CharField(max_length=25, choices=status_choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()


    class Meta:
        verbose_name_plural = "O'qituvchilar"
        ordering = ["last_name"]


class Group(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Document(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class SubmitDocument(models.Model):
    employee = models.ForeignKey(Employee, related_name="employee",  on_delete=models.CASCADE)
    document = models.ForeignKey(Document, related_name="document", on_delete=models.CASCADE)
    group = models.ForeignKey("TeacherGroup", related_name="group", on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)
    status_choices = (
        ("accept", "qabul qilindi"),
        ("reject", "qabul qilinmadi")
    )
    status = models.CharField(max_length=35, choices=status_choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'document', 'group')


    def __str__(self) -> str:
        return self.document.title

    

class TeacherGroup(models.Model):
    employee = models.ForeignKey(Employee, related_name="teacher", on_delete=models.CASCADE)
    teachgroup = models.ForeignKey(Group, related_name="teacher_group", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.teachgroup.title