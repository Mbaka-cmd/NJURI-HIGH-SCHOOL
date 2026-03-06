from django.shortcuts import render, redirect
from django.contrib import messages
from schools.views import admin_required
from students.models import Student
from .sms_utils import send_bulk_sms, format_phone


@admin_required
def bulk_sms(request):
    school = request.user.school
    
    # Get all parents with phone numbers
    from students.models import ParentGuardian
    parents = ParentGuardian.objects.filter(school=school).exclude(phone_primary='')
    total_parents = parents.count()

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        recipient_type = request.POST.get('recipient_type', 'all_parents')
        custom_phones = request.POST.get('custom_phones', '').strip()

        if not message:
            messages.error(request, "Message cannot be empty.")
            return render(request, 'communications/bulk_sms.html', {'total_parents': total_parents, 'parents': parents})

        if len(message) > 160:
            messages.warning(request, f"Message is {len(message)} characters — will be sent as {len(message)//160 + 1} SMS parts.")

        recipients = []

        if recipient_type == 'all_parents':
            for parent in parents:
                try:
                    recipients.append(format_phone(parent.phone_primary))
                except:
                    pass

        elif recipient_type == 'custom':
            for line in custom_phones.splitlines():
                line = line.strip()
                if line:
                    try:
                        recipients.append(format_phone(line))
                    except:
                        pass

        if not recipients:
            messages.error(request, "No valid phone numbers found.")
            return render(request, 'communications/bulk_sms.html', {'total_parents': total_parents, 'parents': parents})

        # Remove duplicates
        recipients = list(set(recipients))

        results = send_bulk_sms(recipients, message)

        context = {
            'total_parents': total_parents,
            'parents': parents,
            'done': True,
            'sent': results['sent'],
            'failed': results['failed'],
            'errors': results['errors'],
            'message_sent': message,
            'total_recipients': len(recipients),
        }
        return render(request, 'communications/bulk_sms.html', context)

    return render(request, 'communications/bulk_sms.html', {
        'total_parents': total_parents,
        'parents': parents,
    })
