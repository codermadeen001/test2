from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.http import require_http_methods
from .models import Field
from users.models import CustomUser
import json
from datetime import datetime

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_field(request):
    try:
        data = request.data
        name = request.data.get('name')
        crop_type = data.get('crop_type')
        planting_date_str = data.get('planting_date')
        agent_id = data.get('assigned_agent_id')
        
        # Validate required fields
        if not name:
            return JsonResponse({
                'success': False,
                'error': 'Name is required'
            }, status=400)
        
        if not crop_type:
            return JsonResponse({
                'success': False,
                'error': 'Crop type is required'
            }, status=400)
        
        if not planting_date_str:
            return JsonResponse({
                'success': False,
                'error': 'Planting date is required'
            }, status=400)
        
        if not agent_id:
            return JsonResponse({
                'success': False,
                'error': 'Assigned agent is required'
            }, status=400)
        
        # Get the agent instance
        try:
            assigned_agent = CustomUser.objects.get(id=agent_id, role='agent')
        except CustomUser.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Agent with id {agent_id} not found'
            }, status=404)
        
        # Validate planting date format
        try:
            planting_date = datetime.strptime(planting_date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }, status=400)
        
        # Create the field
        field = Field.objects.create(
            name=name,
            crop_type=crop_type,
            planting_date=planting_date,
            current_stage=data.get('current_stage', 'Planted'),
            assigned_agent=assigned_agent,
            created_by_admin=request.user
        )
        
        # Return success response
        return JsonResponse({
            'success': True,
            'message': 'Field created successfully',
            'field': {
                'id': field.id,
                'name': field.name,
                'crop_type': field.crop_type,
                'planting_date': field.planting_date.strftime('%Y-%m-%d'),
                'current_stage': field.current_stage,
                'status': field.calculate_status(),
                'assigned_agent_id': field.assigned_agent.id,
                'assigned_agent_name': field.assigned_agent.name,
                'assigned_agent_email': field.assigned_agent.email,
                'created_at': field.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=201)
        
    except Exception as e:
        print(f"Error creating field: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)
    





@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fields(request):

    user =request.user 
    if user.role == 'admin':
        # Admin sees all fields
        fields = Field.objects.all().order_by('-created_at')
    else:
        # Agent sees only assigned fields
        fields = Field.objects.filter(assigned_agent=user.id).order_by('-created_at')
    
    #fields = Field.objects.all().order_by('-created_at')
    fields_data = []
    for field in fields:
        fields_data.append({
            'id': field.id,
            'name': field.name,
            'crop_type': field.crop_type,
            'planting_date': field.planting_date,
            'current_stage': field.current_stage,
            'status': field.calculate_status(),
            'notes':field.notes,
            'assigned_agent_id': field.assigned_agent.id if field.assigned_agent else None,
            'assigned_agent_name': field.assigned_agent.name if field.assigned_agent else None,
            'created_by_admin_id': field.created_by_admin.id if field.created_by_admin else None,
            'updated_at':field.updated_at,
            'created_at': field.created_at
        })
    
    return JsonResponse({'fields': fields_data})







@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_stats(request):
    user = request.user
    if not user:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    if user.role == 'admin':
        fields = Field.objects.all()
    else:
        fields = Field.objects.filter(assigned_agent=user)
    
    total_fields = fields.count()
    status_breakdown = {
        'Active': 0,
        'At Risk': 0,
        'Completed': 0
    }
    stage_breakdown = {
        'Planted': 0,
        'Growing': 0,
        'Ready': 0,
        'Harvested': 0
    }
    
    for field in fields:
        status = field.calculate_status()
        status_breakdown[status] = status_breakdown.get(status, 0) + 1
        stage_breakdown[field.current_stage] = stage_breakdown.get(field.current_stage, 0) + 1
    
    stats = {
        'total_fields': total_fields,
        'status_breakdown': status_breakdown,
        'stage_breakdown': stage_breakdown,
        'role': user.role
    }
    
    return JsonResponse(stats)



#update field
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_field(request, field_id):
    try:
        field = Field.objects.get(id=field_id)
        data = json.loads(request.body)
        
        if 'name' in data:
            field.name = data['name']
        if 'crop_type' in data:
            field.crop_type = data['crop_type']
        if 'planting_date' in data:
            field.planting_date = datetime.strptime(data['planting_date'], '%Y-%m-%d').date()
        if 'assigned_agent_id' in data:
            if data['assigned_agent_id']:
                try:
                    field.assigned_agent = CustomUser.objects.get(id=data['assigned_agent_id'], role='agent')
                except CustomUser.DoesNotExist:
                    return JsonResponse({'error': 'Agent not found'}, status=400)
            else:
                field.assigned_agent = None
        
        field.save()
        
        return JsonResponse({
            'message': 'Field updated successfully'
        })
    except Field.DoesNotExist:
        return JsonResponse({'error': 'Field not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)




@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_field(request, field_id):
    """Delete a field (admin only)"""
    try:
        field = Field.objects.get(id=field_id)
        field_name = field.name
        field.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Field "{field_name}" deleted successfully'
        }, status=200)
        
    except Field.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Field not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)



#updates
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_field_updates(request, field_id):
        updates = Field.objects.filter(id=field_id)
        updates_data = []
        for update in updates:
            updates_data.append({
                'id': update.id,
                'old_stage': update.old_stage,
                'new_stage': update.current_stage,
                'notes': update.notes if update.notes else "No notes",
                'agent_name': update.assigned_agent.name,
                'created_at': update.updated_at
            })
        
        return JsonResponse({'updates': updates_data})





@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_update(request):
    try:
        data = json.loads(request.body)
        
        if 'field_id' not in data or 'new_stage' not in data:
            return JsonResponse({'error': 'field_id and new_stage are required'}, status=400)
        
        try:
            field = Field.objects.get(id=data['field_id'])
        except Field.DoesNotExist:
            return JsonResponse({'error': 'Field not found'}, status=404)
        
        
        # Validate stage transition
        valid_transitions = {
            'Planted': ['Growing'],
            'Growing': ['Ready'],
            'Ready': ['Harvested'],
            'Harvested': []
        }
        
        if data['new_stage'] not in valid_transitions.get(field.current_stage, []):
            return JsonResponse({'error': f'Invalid stage transition from {field.current_stage} to {data["new_stage"]}'}, status=400)
        

        field.old_stage = field.current_stage
        field.current_stage = data['new_stage']
        field.notes=data.get('notes', '')
        field.save()
        
        return JsonResponse({
            'message': 'Field updated successfully',
          
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
