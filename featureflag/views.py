# views.py
import os
import subprocess
import redis
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User

# Initialize a Redis client with the specified host and password
r = redis.Redis(
    host='redis-10120.c321.us-east-1-2.ec2.redns.redis-cloud.com',
    port=10120,
    db=0,
    password='vw7NTK5m3dsYKPg6E5eb1oKXKzCFPLU9',
    decode_responses=True
)

# @api_view(['GET'])
# def get_feature_flag_value(request):
#     key = request.GET.get('key')
#     if key:
#         value = r.get(key)
#         if value:
#             return Response({'value': value})
#         else:
#             return Response({'error': 'No value found for the given key.'}, status=404)
#     else:
#         return Response({'value': 'default_value'})
@api_view(['GET'])
def get_feature_flag_value(request):
    data = request.query_params  # Use query_params to access GET parameters
    keys = data.getlist('key')  # Get a list of all 'key' parameters
    response_data = {}

    for key in keys:
        value = r.get(key)
        if value is not None:
            response_data[key] = value
        else:
            response_data[key] = 'No value found for the given key.'

    return Response(response_data)

@api_view(['POST', 'GET'])
def user_operations(request):
    # Check if the githubaction flag is enabled
    githubaction_flag_status = int(r.get("githubaction") or 0)
    
    if githubaction_flag_status == 1:  # If githubaction flag is enabled
        # Trigger GitHub Actions workflow
        #trigger_github_actions_workflow()
        if request.method == 'POST':  # If request is for user creation
            # Create user with provided data
            # Assuming data is sent in JSON format with keys: name, age, address
            data = request.data
            name = data.get('name')
            age = data.get('age')
            address = data.get('address')
            # Perform user creation logic here
            user = User.objects.create(name=name, age=age, address=address)
            return Response({'message': 'User created successfully.'})
            
        elif request.method == 'GET':  # If request is for user list
            # Fetch and return user list
            user_list = list(User.objects.all().values())  # Fetch user list from database
            return Response({'user_list': user_list})
    else:
        return Response({'message': 'Feature not enabled.'}, status=403)  # Return forbidden status if feature flag is not enabled
    
@api_view(['PUT', 'DELETE'])
def edit_delete_user(request, user_id):
    # Check if the featureflagvalue2 flag is enabled
    featureflagvalue2_flag_status = int(r.get("featureflagvalue2") or 0)
    
    if featureflagvalue2_flag_status == 1:  # If featureflagvalue2 flag is enabled
        if request.method == 'PUT':  # If request is for editing a user
            try:
                # Fetch the user to be edited
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=404)
            
            # Assuming data is sent in JSON format with keys: name, age, address
            data = request.data
            name = data.get('name')
            age = data.get('age')
            address = data.get('address')
            
            # Update the user's data
            user.name = name
            user.age = age
            user.address = address
            user.save()
            
            return Response({'message': 'User updated successfully.'})
            
        elif request.method == 'DELETE':  # If request is for deleting a user
            try:
                # Fetch the user to be deleted
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=404)
            
            # Delete the user
            user.delete()
            
            return Response({'message': 'User deleted successfully.'})
            
    return Response({'message': 'Feature not enabled.'}, status=403)  # Return forbidden status if feature flag is not enabled

def trigger_github_actions_workflow():
    # Command to trigger GitHub Actions workflow
    subprocess.run(['gh', 'workflow', 'run', '-R', 'python_githubaction', 'Run Tests'])

def execute_tests():
    # Command to execute tests
    subprocess.run(['pytest', 'tests/'])

def check_tests_success():
    # Logic to check if tests were successful
    # Assuming tests write output to a file 'test_output.txt' with 'SUCCESS' or 'FAILURE'
    with open('test_output.txt', 'r') as f:
        output = f.read()
        return 'SUCCESS' in output