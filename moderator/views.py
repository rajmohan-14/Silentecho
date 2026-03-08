from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from confessions.models import Post, ModerationQueue
from .utils import mod_required, get_mod_role, is_moderator
from .models import ModRole


def unauthorized(request):
    """Shown when a non-mod tries to access the dashboard."""
    from confessions.models import SessionKindness
    from .utils import KINDNESS_THRESHOLD

    kindness_points = 0
    try:
        kindness        = SessionKindness.objects.get(
            session_token=request.session_token
        )
        kindness_points = kindness.kindness_points
    except SessionKindness.DoesNotExist:
        pass

    context = {
        'kindness_points': kindness_points,
        'threshold':       KINDNESS_THRESHOLD,
        'points_needed':   max(0, KINDNESS_THRESHOLD - kindness_points),
    }
    return render(request, 'moderator/unauthorized.html', context)


@mod_required
def dashboard(request):
    
    mod_role = get_mod_role(request.session_token)

   
    pending = ModerationQueue.objects.filter(
        status='pending'
    ).select_related('post').order_by('created_at')

 
    reviewed = ModerationQueue.objects.filter(
        status__in=['approved', 'rejected']
    ).select_related('post').order_by('-reviewed_at')[:10]

    context = {
        'pending':        pending,
        'reviewed':       reviewed,
        'mod_role':       mod_role,
        'daily_remaining': 10 - (mod_role.actions_today if mod_role else 0),
        'pending_count':  pending.count(),
    }
    return render(request, 'moderator/dashboard.html', context)


@mod_required
def approve_post(request, queue_id):
  
    if request.method == 'POST':
        queue_item = get_object_or_404(ModerationQueue, id=queue_id, status='pending')
        mod_role   = get_mod_role(request.session_token)

        # Check daily limit
        if mod_role.daily_limit_reached:
            return JsonResponse({
                'error': 'Daily action limit reached. Come back tomorrow.'
            }, status=429)

     
        queue_item.post.is_approved = True
        queue_item.post.save()

       
        queue_item.status      = 'approved'
        queue_item.reviewed_at = timezone.now()
        queue_item.save()

        # Log the action
        mod_role.log_action()

        return JsonResponse({
            'status':  'approved',
            'message': 'Post approved and now live on feed',
        })

    return JsonResponse({'error': 'POST required'}, status=405)


@mod_required
def reject_post(request, queue_id):
   
    if request.method == 'POST':
        queue_item = get_object_or_404(ModerationQueue, id=queue_id, status='pending')
        mod_role   = get_mod_role(request.session_token)

        # Check daily limit
        if mod_role.daily_limit_reached:
            return JsonResponse({
                'error': 'Daily action limit reached. Come back tomorrow.'
            }, status=429)

       
        queue_item.post.is_approved = False
        queue_item.post.save()

       
        queue_item.status      = 'rejected'
        queue_item.reviewed_at = timezone.now()
        queue_item.save()

    
        mod_role.log_action()

        return JsonResponse({
            'status':  'rejected',
            'message': 'Post rejected',
        })

    return JsonResponse({'error': 'POST required'}, status=405)