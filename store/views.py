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
    user_rents = []
    if not user_rents:
        return render(request, 'my-rent-empty.html')
    
    return render(request, 'my-rent.html')
    
    


def faq(request):

    return render(request, 'faq.html')
