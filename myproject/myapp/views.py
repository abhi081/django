# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Item
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import CustomAuthenticationForm, CustomUserCreationForm

# Create your views here.


"""
View for handling login or registration.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: The HTTP response object.

Description:
    This view function handles the login or registration process. If the request method is POST,
    it checks if the form data is valid. If it is valid, it logs in the existing user and
    redirects to the 'form' page. If it is not valid, it registers the new user, logs in the user,
    and redirects to the 'form' page. If the request method is not POST, it initializes the form
    for login or registration.

    This function renders the 'login_or_register.html' template and passes the form as context.
"""
def login_or_register_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Login existing user
            user = form.get_user()
            login(request, user)
            return redirect('form')
        else:
            # Registration for new user
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('form')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login_or_register.html', {'form': form})

def check_login_issues(username):
    """
    Checks for possible reasons why a user with the given username cannot log in.

    Args:
        username (str): The username of the user to check.

    Returns:
        str: A message describing the reason for the login issue.
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return "The user does not exist."

    if not user.is_active:
        return "The user account is inactive or has been disabled."

    if not user.has_usable_password():
        return "The user password is not set or unusable."

    # Check if the user is in the admin group or has staff status
    if not user.is_staff or not user.groups.filter(name="Admin").exists():
        return "The user is not showing in admin because they are not marked as staff or not in the Admin group."

    return "The user should be able to log in and appear in admin. Check for issues with the authentication backend."

# Example usage:
# message = check_login_issues('kapil')
# print(message)

"""
This function is a view that handles the rendering and submission of a form. It requires the user to be logged in.

Parameters:
    request (HttpRequest): The HTTP request object that contains metadata about the request.

Returns:
    HttpResponse: The HTTP response object that represents the rendered form template or a redirect to the 'form' URL.
"""
@login_required
def form_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = float(request.POST['price'])
        item = Item(name=name, price=price, user=request.user)
        item.save()
        return redirect('form')

    user_items = Item.objects.filter(user=request.user)
    return render(request, 'form.html', {'items': user_items, 'total_amount': sum(item.price for item in user_items)})


"""
Render a summary view for the authenticated user.
Parameters:
- `request` (HttpRequest): The request object sent to the view.
Returns:
- `HttpResponse`: The response object containing the rendered HTML.
"""
@login_required
def summary_view(request):
    user_items = Item.objects.filter(user=request.user)
    total_amount = sum(item.price for item in user_items)
    return render(request, 'summary.html', {'items': user_items, 'total_amount': total_amount})