from django.urls import path
from .views import create_field, get_fields,update_field, delete_field, get_dashboard_stats, get_field_updates, create_update

urlpatterns = [
    path('create/', create_field),
    path('all/', get_fields),
    path('<int:field_id>/update/', update_field),
    path('<int:field_id>/delete/', delete_field),
    path('dashboard/stats/', get_dashboard_stats),

    #updates urls
    path('create/updates/', create_update),
    path('updates/<int:field_id>/',get_field_updates),
]