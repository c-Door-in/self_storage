from django.shortcuts import render, redirect
from django.contrib.auth import logout


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
    user_rents = [1]
    if not user_rents:
        return render(request, 'my-rent-empty.html')
    # context = {
    #     'containers': [
    #         {
    #             'uuid': ,
    #             'location': ,
    #             'container_num': ,
    #             'started_at': DD.MM.YYYY,
    #             'finished_at': DD.MM.YYYY,
    #             'is_expire': bool,
    #         },
    #         {
    #             ...
    #         }
            
    #     ]
    # }
    return render(request, 'my-rent.html')



def faq(request):
    return render(request, 'faq.html')


def payment(request):
    return render(request, 'index.html')


def log_out(request):
    logout(request)
    return redirect(index)
