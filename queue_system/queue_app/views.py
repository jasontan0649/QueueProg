from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import QueueNumber
from .forms import QueueNumberForm
import qrcode
import qrcode.image.svg
from io import BytesIO

def home(request):
    # Generate QR code for new number
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make('Your URL for new number', image_factory=factory)
    stream = BytesIO()
    img.save(stream)
    svg = stream.getvalue().decode()
    return render(request, 'home.html', {'svg': svg})

def current_number(request):
    # Get the latest active number
    current_number = QueueNumber.objects.filter(is_active=True).first()
    pending_numbers = QueueNumber.objects.filter(is_active=True).order_by('number')
    called_numbers = QueueNumber.objects.filter(is_active=False).order_by('-number')
    return render(request, 'current_number.html', {'pending_numbers': pending_numbers, 'current_number': current_number, 'called_numbers': called_numbers})

def new_number(request):
    if request.method == "POST":
        form = QueueNumberForm(request.POST)
        if form.is_valid():
            # Here we don't save the form yet; we need to add the number.
            new_queue_number = form.save(commit=False)
            
            # Retrieve the last number from the QueueNumber model and increment it
            last_number = QueueNumber.objects.all().order_by('number').last()
            if last_number:
                new_queue_number.number = last_number.number + 1
            else:
                # This means this is the first entry in the queue
                new_queue_number.number = 1
            
            # Now save the new QueueNumber with the generated number
            new_queue_number.save()
            
            # Redirect to a new URL:
            return redirect('number_detail', number=new_queue_number.number)  # Or wherever you want to redirect after creation
    else:
        form = QueueNumberForm()  # An unbound form

    return render(request, 'new_number.html', {'form': form})

# Add a view to show the number details
def number_detail(request, number):
    queue_number = QueueNumber.objects.get(number=number)
    return render(request, 'number_detail.html', {'queue_number': queue_number})

def admin_next(request):
    # Get the earliest active queue number
    earliest_queue = QueueNumber.objects.filter(is_active=True).order_by('created_at').first()

    # If a POST request is made to this view, it means the admin wants to deactivate the number
    if request.method == 'POST' and earliest_queue:
        earliest_queue.is_active = False
        earliest_queue.save()
        return HttpResponseRedirect(reverse('admin_next'))  # Redirect to the same page to show next active queue

    return render(request, 'admin_next.html', {'earliest_queue': earliest_queue})