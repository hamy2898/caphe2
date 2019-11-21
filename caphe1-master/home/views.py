from django.views.generic import TemplateView, CreateView
from  django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Product, Category,BaiViet,Cart
from django.template.loader import render_to_string
from django.http import HttpResponse



from django.contrib.auth import authenticate,login
from django.views import View

from django.http import HttpResponseRedirect

#View đăng ký người dùng
class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

#View đăng ký người dùng thành công
class SignUpDoneView(TemplateView):
    template_name = 'registration/signup_done.html'
    title = 'Signup successful'

#View hiển thị trang chủ (index.html)
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        product = Product.objects.all()[:6]
        context = {
            'categorys': categories,
            'products' : product,
        }
        return context
class CatView(TemplateView):
    template_name = "productcat.html"
    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        product = Product.objects.filter(pk = id)
        context = {
            'categorys2': categories,
            'products2': product,
        }
        return context

def productcat(request,id):
    categories = Category.objects.all()
    procat = Product.objects.filter(category_id=id)

    return render(request, 'productcat.html', {'procat': procat,'categorys2': categories})

class Product1(TemplateView):
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        categories = Category.objects.all()
        product = Product.objects.all()
        context = {
            'categorys1': categories,
            'products1': product,
        }
        return context



def detail(request, pk):
    detail = Product.objects.get(pk=pk)
    context = {
        'detail': detail,
        'id': pk,
        }
    return render(request, 'product_detail.html', context)




class AboutView(TemplateView):
    template_name = "aboutus.html"

    def get_context_data(self, **kwargs):
        context = dict()
        baiviets = BaiViet.objects.all()
        context['baiviets'] = baiviets
        return context


def noidung_baiviet(request, pk):
    baiviet = BaiViet.objects.get(pk=pk)
    # print(binhluans)
    context = {
        'baiviet': baiviet,
        'baiviet_id':pk
        }
    return render(request, 'post.html', context)

class Contact(TemplateView):
    template_name = "contact.html"

cart = {}
def addcart(request):
    if request.is_ajax():
        id = request.POST.get('id')
        num = request.POST.get('num')
        proDetail = Product.objects.get(id = id)
        if id in cart.keys():
            itemCart = {
                'name': proDetail.title,
                'price': proDetail.price,
                'image': str(proDetail.product_img),
                'num': int(cart[id]['num'])+1

            }
        else:
            itemCart = {
                'name': proDetail.title,
                'price': proDetail.price,
                'image': str(proDetail.product_img),
                'num': num
            }
        cart[id] = itemCart
        request.session['cart'] = cart
        cartInfo = request.session['cart']
        #global html
        #print(html)
        html = render_to_string('addcart.html', {'cart' :cartInfo})
    return HttpResponse(html)
def cart(request):
    return render(request,'cart.html')


def search(request):
    try:
        search = request.GET.get('search')
    except:
        search = None
    if search :
        products = Product.objects.filter(title = search)
        context = {'query': search, 'products':products}
        template = 'result.html'
    else:
        template = 'shop.html'
        context = {}
    return render(request,template,context)



