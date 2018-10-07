from django.shortcuts import render, redirect, reverse, HttpResponse


def profile(request):
    redirect_to = request.POST.get('redirect_field_name', request.GET.get('next', ''))
    # return redirect(reverse('blog:index'))
    return redirect(redirect_to)

