from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Course, ContactMessage, Registration

def home(request):
    popular_courses = Course.objects.filter(is_active=True)[:3]
    return render(request, 'core/home.html', {'courses': popular_courses})

def courses(request):
    all_courses = Course.objects.filter(is_active=True)
    return render(request, 'core/courses.html', {'courses': all_courses})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name, email=email, phone=phone, message=message
        )
        messages.success(request, 'Vielen Dank für Ihre Nachricht. Wir werden uns in Kürze bei Ihnen melden.')
        return redirect('contact')
        
    return render(request, 'core/contact.html')

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def dashboard_view(request):
    registrations = Registration.objects.all().order_by('-created_at')
    
    context = {
        'total_registrations': registrations.count(),
        'pending_approvals': registrations.filter(status='Pending').count(),
        'confirmed_registrations': registrations.filter(status='Confirmed').count(),
        'recent_registrations': registrations[:5],
        'registrations': registrations,
    }
    return render(request, 'core/dashboard.html', context)

@csrf_exempt
def api_update_registration(request, reg_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            reg = Registration.objects.get(id=reg_id)
            if new_status in dict(Registration.STATUS_CHOICES):
                reg.status = new_status
                reg.save()
                return JsonResponse({'success': True, 'status': new_status})
        except Registration.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@csrf_exempt
def api_delete_registration(request, reg_id):
    if request.method == 'DELETE':
        try:
            reg = Registration.objects.get(id=reg_id)
            reg.delete()
            return JsonResponse({'success': True})
        except Registration.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
