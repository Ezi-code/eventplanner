from django.core.mail import EmailMessage
from django.conf import settings
from main.models import Attendants, Enquiry
import os
from control.models import Event


def news_letter(email):
    from_email = settings.EMAIL_HOST_USER
    to = email
    subject = "Welcome to the EventPlanner Community!"
    body = f"""Hi [Name],

Thanks for joining the EventPlanner community! We're thrilled to have you on board.

Get ready to receive a fresh dose of Latests evetns and marketting tips delivered to your inbox.  We'll be sharing:

Expert insights and industry trends: Gain valuable knowledge and practical tips from the pros in our field.
Early access to promotions and discounts: Be the first to snag deals on our latest products or services.
Exclusive content: Get a behind-the-scenes look at what we're working on and discover hidden gems you won't find anywhere else.
Here's what you can expect:

You'll receive your first newsletter within a month time. We promise to keep your inbox happy by only sending out emails monthly with the best content we have to offer.
You can always manage your preferences or unsubscribe at any time by clicking the link at the bottom of our emails.

We're excited to share our knowledge and inspiration with you.  Welcome aboard!

Best regards,

The EventPlanner Team"""

    mail = EmailMessage(
        from_email=from_email, to=[to], body=body, reply_to=[to], subject=subject
    )
    mail.send()
    return print("success")


def send_email(event, username, email):
    from_email = settings.EMAIL_HOST_USER
    appname = "EventPlanner"
    subject = f"You're in! Get ready for {event.title} with EventPlanner!"
    message = f"""Congratulations {username}! You're officially registered for {event.title} happening on {event.date} at {event.time} We're thrilled you'll be joining us for what promises to be an amazing event.

To enhance your experience, we recommend using the {appname} app (if you haven't already) for:

Event access: View the event schedule, speaker bios, and important information all in one place.
Networking opportunities: Connect with other attendees and share your excitement!
Real-time updates: Receive notifications about any changes or important announcements from the event organizer.

We can't wait to see you at {event.title}!

Best regards,

The {appname} Team"""
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[email],
        reply_to=[email],
    )
    email.send(fail_silently=False)
    return print({"message": "mail sent successfully", "category": "success"})


def save_new_rsvp(data, event):
    name = data.get("name")
    email = data.get("email")
    phone = data.get("tel")
    ticket = data.get("ticket")
    try:
        new_rsvp = Attendants(
            event=event, name=name, email=email, phone=phone, tickets=ticket
        )
        new_rsvp.full_clean()
        new_rsvp.save()
        send_email(event, name, email)
        return True

    except Exception as e:
        print("error: ", e)
        return False


# def save_new_event(data, file_data, user):
#     organizer = user
#     title = data.get("title")
#     description = data.get("description")
#     localtion = data.get("location")
#     image = handle_uploaded_file(file_data["image"])
#     date = data.get("date")
#     time = data.get("time")
#     details = data.get("details")
#     price_tag = data.get("price")
#     try:
#         new_event = Event(
#             organizer=organizer,
#             title=title,
#             description=description,
#             location=localtion,
#             image=image,
#             date=date,
#             time=time,
#             details=details,
#             price_tag=price_tag,
#         )
#         # new_event.full_clean()
#         # new_event.save()
#         return new_event
#     except Exception as e:
#         print("")


def get_enquriy(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    message = request.POST.get("message")
    enquiry = Enquiry(name=name, email=email, phone=phone, message=message)
    return enquiry
