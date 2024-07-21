from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User

def create_user(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        if name and email:
            User.objects.create(name=name, email=email)
            return redirect('user_list')
    return render(request, 'create_user.html')


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('user_list')
    return render(request, 'delete_user.html', {'user': user})