from django.shortcuts import render, redirect, resolve_url, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from pip._vendor.requests import Response

from .models import Employee, Department
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView, View, DetailView, TemplateView, ListView, UpdateView, DeleteView
from .forms import RegistrationForm, LoginForm, EmployeeForm, DepartmentForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q


# Create your views here.
class Index(TemplateView):
    template_name = 'emsi/home/home.html'


#   Authentication
class Register(CreateView):
    model = get_user_model()
    form_class = RegistrationForm
    template_name = 'emsi/registrations/register.html'
    success_url = reverse_lazy('emsi:login')


class Login_View(LoginView):
    model = get_user_model()
    form_class = LoginForm
    template_name = 'emsi/registrations/login.html'

    def get_success_url(self):
        url = resolve_url('emsi:dashboard')
        return url


class Logout_View(View):

    def get(self, request):
        logout(self.request)
        return redirect('emsi:login', permanent=True)


# Main Board
class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'emsi/dashboard/index.html'
    login_url = 'emsi:login'
    model = get_user_model()
    context_object_name = 'qset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['emp_total'] = Employee.objects.all().count()
        context['dept_total'] = Department.objects.all().count()
        context['admin_count'] = get_user_model().objects.all().count()
        context['workers'] = Employee.objects.order_by('-id')
        return context


# Employee's Controller
class Employee_New(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'emsi/employee/create.html'
    login_url = 'emsi:login'
    redirect_field_name = 'redirect:'


class Employee_All(LoginRequiredMixin, ListView):
    template_name = 'emsi/employee/index.html'
    model = Employee
    login_url = 'emsi:login'
    context_object_name = 'employees'
    paginate_by = 5


class Employee_View(LoginRequiredMixin, DetailView):
    queryset = Employee.objects.select_related('department')
    template_name = 'emsi/employee/single.html'
    context_object_name = 'employee'
    login_url = 'emsi:login'


class Employee_Update(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'emsi/employee/edit.html'
    form_class = EmployeeForm
    login_url = 'emsi:login'


class Employee_Delete(DeleteView):
    model = Employee
    template_name = 'emsi/employee/index.html'
    success_url = reverse_lazy('dashboard:employee')


def emp_delete(request,pk):
    emp_ins = Employee.objects.get(id = int(pk))
    emp_ins.delete()
    return redirect('/dashboard/employee/')


def emp_sort(request,sort):
    emp_all = Employee.objects.all().order_by(sort)
    context = {
        'employees':emp_all
    }
    return render(request,'emsi/employee/index.html',context)





# Department views

class Department_Detail(LoginRequiredMixin, ListView):
    context_object_name = 'employees'
    template_name = 'emsi/department/single.html'
    login_url = 'emsi:login'

    def get_queryset(self):
        queryset = Employee.objects.filter(department=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dept"] = Department.objects.get(pk=self.kwargs['pk'])
        return context


class Department_New(LoginRequiredMixin, CreateView):
    model = Department
    template_name = 'emsi/department/create.html'
    form_class = DepartmentForm
    login_url = 'emsi:login'


class Department_Update(LoginRequiredMixin, UpdateView):
    model = Department
    template_name = 'emsi/department/edit.html'
    form_class = DepartmentForm
    login_url = 'emsi:login'
    success_url = reverse_lazy('emsi:dashboard')


class Salary(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'emsi/Salary/index.html'
    login_url = 'emsi:login'
    context_object_name = 'stfpay'


class Pay(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'emsi/Salary/index.html'
    context_object_name = 'emps'
    login_url = 'emsi:login'
