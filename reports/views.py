from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import LeakReport
from .forms import LeakReportForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils.ai_verification import verify_leak

User = get_user_model()

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def web_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'LogIn was Successful')
            if user.user_type == 'admin':
                return redirect('admin-dashboard')
            elif user.user_type == 'team':
                return redirect('team-dashboard')
            else:
                return redirect('public-dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'main/login.html')

@login_required
def web_logout(request):
    logout(request)
    return redirect('login')

@login_required
def public_dash(request):
    return render(request, 'public/public_dashboard.html')

@login_required
def report_leak(request):
    if request.method == 'POST':
        form = LeakReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            
            # Call your verification function
            is_leak = verify_leak(report.image.path)
            print(f"Leak verification result: {is_leak}")

            report.status = 'verified' if is_leak else 'pending'
            report.save()

            messages.success(request, "Leak report submitted successfully.")
            return redirect('public-dashboard')
    else:
        form = LeakReportForm()
    return render(request, 'public/report_form.html', {'form': form})

def my_reports(request):
   my_reports = LeakReport.objects.filter(reporter=request.user).order_by('-created_at')
   return render(request, 'public/my_reports.html', {'reports': my_reports})

@login_required
def admin_dash(request):
    reports = LeakReport.objects.all().order_by('-created_at')
    return render(request, 'admin/admin_dashboard.html', {'reports': reports})

@login_required
def assign_report(request, report_id):
    report = get_object_or_404(LeakReport, id=report_id)
    if request.method == 'POST':
        user_id = request.POST.get('assigned_to')
        assigned_user = User.objects.get(id=user_id)
        report.assigned_to = assigned_user
        report.status = 'assigned'
        report.save()
        return redirect('admin-dashboard')

    team_members = User.objects.filter(user_type='team')
    return render(request, 'admin/assign.html', {
        'report': report,
        'team_members': team_members
    })

@login_required
def team_dash(request):
    my_assignments = LeakReport.objects.filter(assigned_to=request.user).order_by('-created_at')
    return render(request, 'team/team_dashboard.html', {'assignments': my_assignments})

@login_required
def resolve(request, report_id):
    report = get_object_or_404(LeakReport, id=report_id)
    report.status = 'resolved'
    report.save()
    return redirect('team-dashboard')
