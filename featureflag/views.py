# views.py

from django.http import HttpResponse
from .cf_client_configuration import cf_client

def index(request):
    # Initialize CfClient using the API key
    api_key = "your_api_key_here"
    client = cf_client(api_key)

    # Get the status of the feature flag
    flag_name = "your_flag_name_here"
    flag_enabled = client.bool_variation(flag_name, None, False)

    # Your business logic based on the feature flag status
    if flag_enabled:
        # Feature flag is enabled, execute code accordingly
        response = "Feature flag is enabled. Performing enabled action..."
    else:
        # Feature flag is disabled, execute alternative code
        response = "Feature flag is disabled. Performing alternative action..."

    return HttpResponse(response)



# from django.shortcuts import render
# from .cf_client_configuration import CfClientConfiguration

# def index(request):
#     # Instantiate CfClientConfiguration and get feature flag status
#     cf_client = CfClientConfiguration()
#     cf_client.get_feature_flag_status()

#     # Retrieve the feature flag status and pass it to the template
#     flag_status = "Enabled"  # Replace with the actual flag status obtained from CfClientConfiguration
#     context = {'flag_status': flag_status}

#     return render(request, 'index.html', context)
