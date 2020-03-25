from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from mapview.utils import plzs, get_plzs_close_to
from .tables import StudentTable
from .filters import StudentFilter

from .forms import StudentForm, EmailToSendForm, EmailForm
from .models import Student, EmailToSend
from match4healthcare.settings.common import NOREPLY_MAIL

from apps.ineedstudent.forms import HospitalFormExtra
from apps.ineedstudent.models import Hospital

from django.contrib.auth.decorators import login_required
from apps.accounts.decorator import student_required, hospital_required


def get_student(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('thanks')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'student.html', {'form': form})


def thx(request):
    return render(request, 'thanks.html')


def successful_mail(request):
    return render(request,'emails_sent.html')


def send_mail_student(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            notify_student(form.cleaned_data['student_id'], form.cleaned_data['contact_adress'])

            return HttpResponseRedirect('successful_mail')

    else:
        form = EmailForm()
    return render(request, 'mail.html', {'form': form})


@login_required
@hospital_required
def send_mail_student_id_list(request, id_list):
    id_list = id_list.split('_')

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmailToSendForm(request.POST)

        if form.is_valid():
            # todo check header injections!!!!
            hospital_message = form.cleaned_data['message']



            subject = form.cleaned_data['subject']
            for student_id in id_list:
                student = Student.objects.get(user_id=student_id)

                message = 'Hallo %s %s,\n\n wir haben folgende Nachricht von %s für dich.\n\nDein Match4MedisTeam\n\n%s' % (
                    student.name_first,
                    student.name_last,
                    request.user.hospital.firmenname,
                    hospital_message
                )

                mail = EmailToSend.objects.create(
                    student=student,
                    hospital=request.user.hospital,
                    message=message,
                    subject=subject)
                mail.save()
            if request.user.hospital.is_approved:
                send_mails_for(request.user.hospital)
            return HttpResponseRedirect('/iamstudent/successful_mail')
    else:
        hospital = request.user.hospital
        form = EmailToSendForm(initial={'subject': '[Match4Medis] Ein Ort braucht Deine Hilfe',
                                        'message': 'Liebe Helfer,\n\nWir sind... \nWir suchen...\n\nMeldet euch baldmöglichst!\n\nBeste Grüße,\n%s\n\nTel: %s\nEmail: %s'%(hospital.ansprechpartner,hospital.telefon,hospital.user.email)})

    return render(request, 'send_mail_hospital.html', {'form': form, 'ids': '_'.join(id_list), 'n': len(id_list)})


def send_mails_for(hospital):
    emails = EmailToSend.objects.filter(hospital=hospital, was_sent=False)
    for m in emails:
        send_mail(m.subject,
                  m.message,
                  NOREPLY_MAIL,
                  [m.student.user.email]
                  )
        m.was_sent = True
        m.save()


def notify_student(student_id, contact):
    student = Student.objects.get(id=student_id)
    send_mail(subject=_('subject :)'),
              message=_('I want to hire you person of gender %s!, Contact me here: %s') % (student.gender, contact),
              from_email='noreply@medisvs.spahr.uberspace.de',
              recipient_list=[student.email])

@login_required
@hospital_required
def student_list_view(request, countrycode, plz, distance):
    print('start')
    if countrycode not in plzs or plz not in plzs[countrycode]:
        # TODO: niceren error werfen
        return HttpResponse("Postleitzahl: " + plz + " ist keine valide Postleitzahl in " + countrycode)
    print('---')
    lat, lon, ort = plzs[countrycode][plz]

    # TODO Consult with others how this should behave!
    if distance==0:
        qs = Student.objects.filter(plz=plz, countrycode=countrycode)
    else:
        close_plzs = get_plzs_close_to(countrycode, plz, distance)
        qs = Student.objects.filter(plz__in=close_plzs, countrycode=countrycode)
    print('---')
    table = StudentTable(qs)
    filter = StudentFilter(request.GET, queryset=Student.objects.all())

    context = {
        'plz': plz,
        'countrycode': countrycode,
        'ort': ort,
        'distance': distance,
        'table': table,
        'filter': filter
    }

    return render(request, 'student_list_view.html', context)


