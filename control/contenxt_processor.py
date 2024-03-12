from main.models import Enquiry


def get_notification(request):
    enquiries = Enquiry.objects.filter(read=False).count()
    messages = Enquiry.objects.filter(read=False).all()
    return {"enquiries": enquiries, "messages": messages}
