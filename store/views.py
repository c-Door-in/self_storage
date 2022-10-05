from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


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


@login_required
def my_rent(request):
    user_rents = [1]
    if not user_rents:
        return render(request, 'my-rent-empty.html')
    # context = {
        # 'user': {
        #     'email':
        #     'phone':
        #     'password':
        #     'name':
        #     'photo':
        # }
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


@login_required
def payment(request):
    return render(request, 'index.html')


@login_required
def log_out(request):
    logout(request)
    return redirect(index)
