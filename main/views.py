from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from .models import Employee, Document, SubmitDocument, TeacherGroup, Group
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def update_employee_status(employee_id):
    employee = Employee.objects.get(pk=employee_id)
    all_groups = employee.teacher.all()
    documents = Document.objects.all().count()
    a = 0
    for group in all_groups:
        documents_count = SubmitDocument.objects.filter(employee=employee, group=group).count()
        if documents_count == documents:
            a = a + 1  # Specify the total number of documents required for each group
        

    if a == len(all_groups):
        employee.status = "active"
        employee.save()
    elif a < len(all_groups):
        employee.status = "inactive"
        employee.save()

@login_required(login_url="/admin")
def index(request):
    items_per_page = 10
    employees = Employee.objects.all().order_by("last_name")
    for employee in employees:
        update_employee_status(employee.id)
    search_query = request.GET.get('search', '')
    sort = request.GET.get('sort', '')
    if sort and search_query:
        employees = employees.filter(first_name__icontains=search_query) | employees.filter(last_name__icontains=search_query)
        employees.filter(status=sort).order_by("last_name")

    if search_query:
        employees = employees.filter(first_name__icontains=search_query) | employees.filter(last_name__icontains=search_query) | employees.filter(pass_number__icontains=search_query)
    
    if sort:
        employees = employees.filter(status=sort).order_by("last_name")
    paginator = Paginator(employees, items_per_page)
    page_number = request.GET.get("page", 1)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, "index.html", {"employees": page})


def detail(request, id):
    employee = get_object_or_404(Employee, id=id)
    documents = Document.objects.all()
    groups = TeacherGroup.objects.filter(employee=employee).order_by('updated')
    update_employee_status(employee.id)
    selected_group = None
    grs = Group.objects.all()
    all_groups = list()
    for g in grs:
        if g not in groups.values_list("teachgroup__id", flat=True):
            all_groups.append(g)

    if request.method == "GET":
        selected_group_id = request.GET.get("group", "")
        if selected_group_id:
            try:
                selected_group = TeacherGroup.objects.get(id=int(selected_group_id))
            except TeacherGroup.DoesNotExist:
                pass

        if not selected_group and groups.exists():
            selected_group = groups.last()
        submit_documents = SubmitDocument.objects.filter(employee=employee, group=selected_group)
        submitted_document_ids = list(submit_documents.values_list('document__id', flat=True))
        return render(request, "detail.html", {
            "employee": employee,
            "groups": groups,
            "documents": documents,
            "submit_documents": submit_documents,
            "selected_group": selected_group,
            "submitted_document_ids": submitted_document_ids,
            'all_groups': all_groups
        })
    elif request.method == "POST":
        update_employee_status(employee.id)
        submitted_documents = request.POST.getlist("submitted_documents")
        selected_group_id = request.POST.get("selected_group")
        if not selected_group_id:
            messages.error(request, "Guruh tanlanmagan!")
            return redirect("document", employee.id)
        group = TeacherGroup.objects.get(id=int(selected_group_id))

        existing_submissions = SubmitDocument.objects.filter(employee=employee, group=group)

        unchecked_document_ids = set(existing_submissions.values_list('document__id', flat=True)) - set(map(int, submitted_documents))

        existing_submissions.filter(document__id__in=unchecked_document_ids).delete()

        for doc_id in submitted_documents:
            if int(doc_id) not in existing_submissions.values_list('document__id', flat=True):
                document = Document.objects.get(id=int(doc_id))
                SubmitDocument.objects.create(employee=employee, group=group, document=document)
        
        messages.success(request, "Changes saved successfully!")
        
        return render(request, "detail.html", {
            "employee": employee,
            "groups": groups,
            "documents": documents,
            "submit_documents": existing_submissions,
            "selected_group": group,
            "submitted_document_ids": existing_submissions.values_list('document__id', flat=True),
            'all_groups': all_groups
        })
        # return redirect('document', employee.id)
        # return HttpResponseRedirect(reverse("document", args=(employee.id,)))



def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        citizenship = request.POST.get('citizen')
        pass_number = request.POST.get('passport')
        pass_date = request.POST.get('pass_date')
        jshshir = request.POST.get('jshshr')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        birth_date = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        village = request.POST.get('village')
        city = request.POST.get('city')
        live_village = request.POST.get('live_village')
        live_city = request.POST.get('live_city')
        live_mfy = request.POST.get('live_mfy')
        live_street = request.POST.get('live_street')
        live_home = request.POST.get('live_home')
        edu_country = request.POST.get('study_country')
        edu_name = request.POST.get('stydy_univer')
        speciality = request.POST.get('speciality')
        edu_degree = request.POST.get('degree')

        employee = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            citizenship=citizenship,
            pass_number=pass_number,
            pass_date=pass_date,
            jshshir=jshshir,
            email=email,
            phone_number=phone_number,
            birth_date=birth_date,
            gender=gender,
            country=country,
            village=village,
            city=city,
            live_village=live_village,
            live_city=live_city,
            live_mfy=live_mfy,
            live_street=live_street,
            live_home=live_home,
            edu_country=edu_country,
            edu_name=edu_name,
            speciality=speciality,
            edu_degree=edu_degree,
            status="inactive",
        )
        messages.success(request, "Muvafaqqiyatli saqlandi!")
        return redirect("index")

    return render(request, 'registration.html')



def connect_group(request):
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        groups = request.POST.getlist('groups')
        if not groups:
            messages.error(request, "Avval guruh qo'shing")
            return redirect(redirect_url)
        employee_id = request.POST.get('employee')
        employee = get_object_or_404(Employee, pk=int(employee_id))
        for group in groups:
            gr = get_object_or_404(Group, pk=int(group))
            if not TeacherGroup.objects.filter(employee=employee, teachgroup=gr).exists():
                TeacherGroup.objects.create(employee=employee, teachgroup=gr)
        messages.success(request, "Guruh biriktirildi!")

        return redirect(redirect_url)
    return redirect("index")



def documents(request):
    documents = Document.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        d = Document.objects.create(title=title)
        messages.success(request, "Hujjat qo'shildi")
        return redirect("documents")
    return render(request, "documents.html", {'documents': documents})


def delete_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    document.delete()
    messages.success(request, "Hujjat o'chirildi!")
    return redirect("documents")


def groups(request):
    groups = Group.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        gr = Group.objects.create(title=title)
        messages.success(request, "Guruh qo'shildi!")
        return redirect("groups")

    return render(request, 'groups.html', {'groups': groups})


def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    messages.success(request, "Guruh o'chirildi")
    return redirect("groups")
