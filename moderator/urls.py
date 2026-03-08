from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.dashboard,    name='mod_dashboard'),
    path('unauthorized/',            views.unauthorized, name='mod_unauthorized'),
    path('approve/<int:queue_id>/',  views.approve_post, name='mod_approve'),
    path('reject/<int:queue_id>/',   views.reject_post,  name='mod_reject'),
]