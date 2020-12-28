from django.shortcuts import render,  redirect
from django.core.mail import send_mail
from .forms import ContactForm

def send_msg(name, email, subject, body):
    return 
    # to = ["stepina.m.p@gmail.com", ]
    # send_mail(
    #     subject, body, email, to,
    # )


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid:
            name = form['name']
            email = form['email']
            subject = form['subject']
            message = form['body']    
            form.save()  
            # send_msg(name, email, subject, message)
            return redirect('/contact/thank-you/')
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def thank_you(request):
    return render(request, "thank-you.html")

