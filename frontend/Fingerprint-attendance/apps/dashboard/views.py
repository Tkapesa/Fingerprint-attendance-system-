from django.shortcuts import render

def dashboard(request):
    user_name = request.session.get('user_name', 'Guest')
    user_role = request.session.get('user_role', 'None')
    
    context = {
        'message': f'Welcome {user_name}!',
        'user_role': user_role
    }
    
    return render(request, 'dashboard/dashboard.html', context)
