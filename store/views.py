from django.shortcuts import render


def save_email_if_sent(request):
    email = request.GET.get('EMAIL1')
    if not email:
        return
    # save email if valid else pass


def index(request):
    save_email_if_sent(request)
    return render(request, 'index.html')


def boxes(request):
    save_email_if_sent(request)
    return render(request, 'boxes.html')


def my_rent(request):

    return render(request, 'my-rent.html')


def my_rent_empty(request):

    return render(request, 'my-rent-empty.html')


def faq(request):

    return render(request, 'faq.html')
