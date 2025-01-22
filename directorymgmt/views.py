from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from dmapp.models import CustomUser,directory
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.db.models import Q
User = get_user_model()

def BASE(request):
       return render(request,'base.html')






def Index(request):
    # Retrieve all data with status='1'
    data_list = directory.objects.filter(status='1')

    # Check if a search query is present in the request
    query = request.GET.get('query', '')
    if query:
        # Perform search and maintain status='1'
        data_list = directory.objects.filter(
            Q(fullname__icontains=query) |
            Q(mobilenumber__icontains=query) |
            Q(email__icontains=query),
            status='1'
        )
        messages.info(request, "Search against " + query)

    # Pagination
    paginator = Paginator(data_list, 6)  # Show 6 data per page
    page_number = request.GET.get('page')
    try:
        data_list = paginator.page(page_number)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    context = {'data_list': data_list, 'query': query}
    return render(request, 'index.html', context)


@login_required(login_url = '/')
def DASHBOARD(request):
       allrecord = directory.objects.all().count
       pubrecord = directory.objects.filter(status='1').count
       prirecord = directory.objects.filter(status='2').count
       context = {
    'allrecord':allrecord,
    'pubrecord':pubrecord,
    'prirecord':prirecord,
           
    }
       return render(request,'dashboard.html',context)


def LOGIN(request):
    return render(request,'login.html')

def doLogout(request):
    logout(request)
    request.session.flush()  # Clear the session including CSRF token
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
       

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('dashboard')
            elif user_type == '2':
                return redirect('dashboard')
        else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')  # Redirect back to the login page with an error message
    else:
        # If the request method is not POST, redirect to the login page with an error message
        messages.error(request, 'Invalid request method')
        return redirect('login')



login_required(login_url='/')
def ADMIN_PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'admin_profile.html',context)


@login_required(login_url = '/')
def ADMIN_PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print(profile_pic)
        

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            

            
            if profile_pic !=None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your profile has been updated successfully")
            return redirect('admin_profile')

        except:
            messages.error(request,"Your profile updation has been failed")
    return render(request, 'admin_profile.html')


login_required(login_url='/')
def CHANGE_PASSWORD(request):
    context = {}
    ch = User.objects.filter(id=request.user.id)

    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context["data"] = data  # Corrected this line

    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)

        if check == True:
            user.set_password(new_pas)
            user.save()
            messages.success(request, 'Password Changed Successfully!!!')
            user = User.objects.get(username=un)
            login(request, user)
        else:
            messages.error(request, 'Current Password is incorrect!!!')
            return redirect("change_password")

    return render(request, 'change-password.html', context)




def ADD_DATA(request):
    if request.method == "POST":
        try:
            directory_obj = directory(
                fullname=request.POST['fullname'],
                profession=request.POST['profession'],
                email=request.POST['email'],
                mobilenumber=request.POST['mobilenumber'],
                city=request.POST['city'],
                address=request.POST['address'],
                status=request.POST['status'],
            )
            directory_obj.save()
            messages.success(request, "Directory entry created successfully")
            return redirect('add_data')
        except IntegrityError:
            messages.error(request, "Email must be unique")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, 'add_data.html')

login_required(login_url='/')
def MANAGE_DATA(request):
    data_list = directory.objects.all()
    paginator = Paginator(data_list, 10)  # Show 10 data per page

    page_number = request.GET.get('page')
    try:
        data_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_list = paginator.page(paginator.num_pages)

    context = {'data_list': data_list,
   }
    return render(request, 'manage-data.html', context)

login_required(login_url='/')
def DELETE_DATA(request,id):
       del_data = directory.objects.get(id = id)
       del_data.delete()
       messages.success(request,'Record Delete Succeesfully!!!')
       return redirect('manage_data')

login_required(login_url='/')
def VIEW_DATA(request,id):    
    data_det = directory.objects.get(id =id)    
    context = {
        
        "data_det":data_det,
    }
    return render(request,'update_data.html',context)




@login_required(login_url='/')
def EDIT_DATA(request):
    if request.method == "POST":
        data_id = request.POST.get('data_id')
        try:
            data_edit = directory.objects.get(id=data_id)
        except directory.DoesNotExist:
            messages.error(request, "Data does not exist")
            return redirect('manage_data')

        # Create a dictionary with updated data
        updated_data = {
            'fullname': request.POST.get('fullname'),
            'profession': request.POST.get('profession'),
            'email': request.POST.get('email'),
            'mobilenumber': request.POST.get('mobilenumber'),
            'city': request.POST.get('city'),
            'address': request.POST.get('address'),
            'status': request.POST.get('status'),
        }

        # Update the data_edit object with the updated data
        for field, value in updated_data.items():
            setattr(data_edit, field, value)

        data_edit.save()
        messages.success(request, "Data has been updated successfully")
        return redirect('manage_data')

    return render(request, 'manage-data.html')


login_required(login_url='/')
def ALL_RECORDS(request):
    data_list = directory.objects.all()
    paginator = Paginator(data_list, 10)  # Show 10 data per page

    page_number = request.GET.get('page')
    try:
        data_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_list = paginator.page(paginator.num_pages)

    context = {'data_list': data_list,
   }
    return render(request, 'all-records.html', context)


login_required(login_url='/')
def PUBLIC_RECORDS(request):
    data_list = directory.objects.filter(status='1')
    paginator = Paginator(data_list, 10)  # Show 10 data per page

    page_number = request.GET.get('page')
    try:
        data_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_list = paginator.page(paginator.num_pages)

    context = {'data_list': data_list,
   }
    return render(request, 'public-records.html', context)

login_required(login_url='/')
def PRIVATE_RECORDS(request):
    data_list = directory.objects.filter(status='2')
    paginator = Paginator(data_list, 10)  # Show 10 data per page

    page_number = request.GET.get('page')
    try:
        data_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data_list = paginator.page(paginator.num_pages)

    context = {'data_list': data_list,
   }
    return render(request, 'private-records.html', context)


def SEARCH_RECORDS(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where email or mobilenumber contains the query
            searchdata = directory.objects.filter(fullname__icontains=query) |  directory.objects.filter(mobilenumber__icontains=query)| directory.objects.filter(email__icontains=query)
            
           
            messages.info(request, "Search against " + query)
            return render(request, 'search.html', {'searchdata': searchdata, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'search.html', {})

def RECORDS_REPORTS(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    datarecords = []

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'between-dates-record.html', {'datarecords': datarecords, 'error_message': 'Invalid date format'})

        # Filter visitors between the given date range
        datarecords = directory.objects.filter(creationdate__range=(start_date, end_date))

    return render(request, 'between-dates-record.html', {'datarecords': datarecords,'start_date':start_date,'end_date':end_date})



    
       