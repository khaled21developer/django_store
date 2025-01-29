from django.contrib import admin
from . import models
from .models import SupportRequest
from django.urls import path
from django.shortcuts import render, redirect
from .forms import EmailForm

from django.contrib import admin
from django.contrib.auth.models import User
from .admin import CustomUserAdmin

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'amount', 'payment_method', 'country', 'phone', 'items', 'created_at']
    list_per_page = 20
    list_select_related = ['transaction', 'customer']  # إضافة customer هنا

    def country(self, obj):
        return obj.transaction.customer['country'] if obj.transaction else None  # استخدام customer للحصول على country

    def phone(self, obj):
        return obj.transaction.customer['phone'] if obj.transaction else None  # عرض رقم الهاتف

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def amount(self, obj):
        return obj.transaction.amount

    def items(self, obj):
        return len(obj.transaction.items)

    def email(self, obj):
        return obj.transaction.customer_email

    def payment_method(self, obj):
        return obj.transaction.get_payment_method_display()

@admin.register(models.OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'message']


class CustomUserAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'send-email/',
                self.admin_site.admin_view(self.send_email_view),
                name='send_email'
            ),
        ]
        return custom_urls + urls

    def send_email_view(self, request):
        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                users = form.cleaned_data['users']

                for user in users:
                    user.email_user(subject, message)

                self.message_user(request, "تم إرسال الإيميلات بنجاح!")
                return redirect('..')
        else:
            form = EmailForm()

        context = {
            'form': form,
            'opts': self.model._meta,
        }
        return render(request, 'admin/custom_email_view.html', context)
