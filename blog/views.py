from django.shortcuts import render


def homepage(request):
    """
    Blog homepage.
    """

    return render(request, 'blog/index.html')
