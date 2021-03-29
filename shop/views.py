from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.views.generic import FormView
from django.views.generic.detail import DetailView

from .forms import RegistrationForm, LoginForm, GoodAddForm
from .tokens import account_activation_token
from .models import Product, Cart, Category


class RegistrationView(CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'registration.html'
    success_url = '/login'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.cart_set = Cart(user_id=self.object)
        self.object.cart_set.save()
        self.object.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your profile'
        message = render_to_string(
                'email_confirmation_message.html',
                {
                    'user': self.object,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(self.object.id)),
                    'token': account_activation_token.make_token(self.object)
                }
        )
        to_email = self.object.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/aboutme'
    redirect_authenticated_user = 'aboutme'

    def get_success_url(self):
        return self.success_url


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = 'client.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = User.objects.filter(id=self.request.user.id).first()
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class ActivationView(TemplateView):
    template_name = 'activation.html'

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs['id']))
            self.user = User.objects.filter(id=uid).first()
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None
        if self.user is not None and account_activation_token.check_token(self.user, self.kwargs['token']):
            self.user.is_active = True
            self.user.save()
            login(request, self.user)
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)


class GoodsListView(ListView):
    template_name = 'goods/all_goods.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['cart'] = Cart.objects.filter(user_id=self.request.user).first()
        context['categories'] = Category.objects.all()
        context['goods'] = Product.objects.all()
        return context


class AddProductView(LoginRequiredMixin, FormView):
    form_class = GoodAddForm
    template_name = 'goods/good_add.html'
    success_url = '/goods'
    login_url = '/login'

    def form_valid(self, form):
        self.object = form.save(commit=True)
        return super().form_valid(form)


class DeleteFromCart(LoginRequiredMixin, RedirectView):
    url = '/goods/'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        user = request.user
        product = Product.objects.filter(id=kwargs['id']).first()
        if product:
            user.cart.products.remove(product)
        return super().get(request, *args, **kwargs)


class AddToCart(LoginRequiredMixin, RedirectView):
    url = '/all_goods/'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        user = request.user
        product = Product.objects.filter(id=kwargs['id']).first()
        user.cart.products.add(product)
        return super().get(request, *args, **kwargs)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['products'] = user.cart.products.all()
        context['sum'] = sum([product.price for product in context['products']])
        return context


class CategoryProductList(TemplateView):
    template_name = 'categories/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['cart'] = Cart.objects.filter(user_id=self.request.user).first()
        category = Category.objects.filter(id=kwargs['id']).first()
        context['categories'] = Category.objects.all()
        context['products'] = category.products.all()
        return context
