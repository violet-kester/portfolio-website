from django.shortcuts import render


def homepage(request):
    """
    Homepage.
    """

    return render(request, './core/index.html')
