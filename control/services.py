import os
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from control.models import Event
from settings import base


def update_event(event, request):
    event.title = request.POST.get("title")
    event.description = request.POST.get("description")
    event.location = request.POST.get("location")
    event.date = request.POST.get("date")
    event.time = request.POST.get("time")
    event.details = request.POST.get("details")
    event.price_tag = request.POST.get("price")
    event.image = request.FILES.get("image")
    return event


def handle_uploaded_file(f):
    # Get the file extension
    ext = os.path.splitext(f.name)[1]
    filename = os.path.basename(f.name)
    # Define a list of allowed extensions
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif"]

    # Check if the file has an allowed extension
    if ext.lower() not in allowed_extensions:
        raise ValidationError("Unsupported file extension.")

    # Generate a random string
    random_str = get_random_string(length=32)

    # Create a new filename using the random string
    filename = slugify(filename) + "_" + random_str + ext

    print("filename: ", filename)

    path = base.MEDIA_ROOT + "/" + filename
    print("path: ", path)
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return filename


def save_new_event(data, file_data, user):
    organizer = user
    title = data.get("title")
    description = data.get("description")
    localtion = data.get("location")
    image = handle_uploaded_file(file_data["image"])
    date = data.get("date")
    time = data.get("time")
    details = data.get("details")
    price_tag = data.get("price")
    try:
        new_event = Event(
            organizer=organizer,
            title=title,
            description=description,
            location=localtion,
            image=image,
            date=date,
            time=time,
            details=details,
            price_tag=price_tag,
        )
        # new_event.full_clean()
        # new_event.save()
        return new_event
    except Exception as e:
        print("")
