from django.shortcuts import render

# Create your views here.

# def usual_login_view(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         OneTimeCode.objects.create(code=random.choice('abcde', user=user))
#         send one-time code to email
#         login(request, None)
#         redirect to a succes url
#     else:
#         return an 'invalid login' error message
#
#
# def login_with_view_code(request):
#     username = request.POST['username']
#     code = request.POST['code']
#     if OneTimeCode.objects.filter(code=code, user__username = username).exists():
#         login(request, user)
#     else:
#         error
#     login(request, user)

