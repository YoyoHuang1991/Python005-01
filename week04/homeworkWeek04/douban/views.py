from django.shortcuts import render
from .models import Comments
# Create your views here.
# def index(request):
#     n = Comments.objects.filter(star__gte='4')
#     return render(request, 'index.html', locals())

def index(request):
    #獲取查詢關鍵字
    q = request.GET.get('q')

    error_msg=''

    if not q:
        c_lst = Comments.objects.filter(star__gte='4')
        return render(request, 'index.html', locals())
    
    c_lst = Comments.objects.filter(content__icontains=q)
    if len(c_lst) == 0:
        error_msg='沒有與關鍵字相符的結果'
    return render(request, 'index.html', {'error_msg':error_msg, 'c_lst':c_lst})