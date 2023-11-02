from django.shortcuts import render,redirect
from . models import User,Product
import requests
import random
# Create your views here.
def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Already Registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                    profile_pic=request.FILES['profile_pic'],
                    usertype=request.POST['usertype'],
                )
                msg="User signup successfully"
                return render(request,'signup.html',{'msg':msg})
            else:
                msg="Password and Confirm Password Does not matched!"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')
    
def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                if user.usertype=="buyer":
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    request.session['profile_pic']=user.profile_pic.url
                    return render(request,'index.html')
                else:
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    request.session['profile_pic']=user.profile_pic.url
                    return render(request,'seller_index.html')
            else:
                msg="Incorrect Password"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email Not Registered"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
    
def logout(request):
    try:
        del request.session['fname']
        del request.session['email']
        return render(request,'login.html')
    except:
        return render(request,'login.html')
    
def change_password(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
       
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
                msg="New Password and Confirm New Password Does not Matched!"
                if user.usertype=="buyer":
                    return render(request,'change_password.html',{'msg':msg})
                else:
                    return render(request,'seller_change_password.html',{'msg':msg})
        else:
            msg="Old Password is Incorrect"
            if user.usertype=="buyer":
                    return render(request,'change_password.html',{'msg':msg})
            else:
                    return render(request,'seller_change_password.html',{'msg':msg})
           
    else:
         if user.usertype=="buyer":
                return render(request,'change_password.html')
         else:
            return render(request,'seller_change_password.html')
       
    
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        try:
            user.profile_pic=request.FILES['profile_pic']
        except:
            pass
        user.save()
        msg="Profile Updated Successfully"
        if user.usertype=="buyer":
            return render(request,'profile.html',{'user':user,'msg':msg})
        else:
            return render(request,'seller_profile.html',{'user':user,'msg':msg})
    else:
        if user.usertype=="buyer":
            return render(request,'profile.html',{'user':user})
        else:
            return render(request,'seller_profile.html',{'user':user})
    
def forgot_password(request):
    if request.method=="POST":
        mobile=request.POST['mobile']
        try:
            user=User.objects.get(mobile=mobile)
            otp=random.randint(1000,9999)
            url = "https://www.fast2sms.com/dev/bulkV2"

            querystring = {"authorization":"eYLHjNJ923XdpuOB7gqnTlVPD5FzEUwQ6abGAkR0McrKSIvWimqiMTAY02jxVCHLf8rUQ5BnsJ4PX3Nb","variables_values":str(otp),"route":"otp","numbers":str(mobile)}

            headers = {
            'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            return render(request,'otp.html',{'otp':otp,'mobile':mobile})
        except:
            msg="Mobile Not Registered" 
            return render(request,'forgot_password.html',{'msg':msg})
    else:
        return render(request,'forgot_password.html')
    
def verify_otp(request):
    otp=request.POST['otp']
    uotp=request.POST['uotp']
    mobile=request.POST['mobile']

    if otp==uotp:
        return render(request,'new_password.html',{'mobile':mobile})
    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'otp':otp,'mobile':mobile,'msg':msg})
    
def new_password(request):
    mobile=request.POST['mobile']
    np=request.POST['new_password']
    cnp=request.POST['cnew_password']

    if np==cnp:
        user=User.objects.get(mobile=mobile)
        user.password=np
        user.save()
        msg="Password Updated Successfully"
        return render(request,'login.html',{'msg':msg})
    else:
        msg="New Password and Confirm New Passoword does not matched"
        return render(request,'new_password.html',{'mobile':mobile,'msg':msg})
    
def seller_index(request):
    return render(request,'seller_index.html')

def seller_add_product(request):
    seller=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        Product.objects.create(
            seller=seller,
            product_category=request.POST['product_category'],
            product_name=request.POST['product_name'],
            product_price=request.POST['product_price'],
            product_desc=request.POST['product_desc'],
            product_image=request.FILES['product_image'],
        )
        msg="Product Added Successfully"
        return render(request,'seller_add_product.html',{'msg':msg})
    else:
        return render(request,'seller_add_product.html')
    
def seller_view_product(request):
    seller=User.objects.get(email=request.session['email'])
    products=Product.objects.filter(seller=seller)
    return render(request,'seller_view_product.html',{'products':products})

def seller_product_details(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'seller_product_details.html',{'product':product})

def seller_edit_product(request,pk):
    product=Product.objects.get(pk=pk)

    if request.method=="POST":
        product.product_category=request.POST['product_category']
        product.product_name=request.POST['product_name']
        product.product_price=request.POST['product_price']
        product.product_desc=request.POST['product_desc']

        try:
            product.product_image=request.FILES['product_image']
        except:
            pass
        product.save()
        msg="Product Edited Successfully"
        return render(request,'seller_edit_product.html',{'product':product,'msg':msg})
    else:
        return render(request,'seller_edit_product.html',{'product':product})
    
def seller_delete_product(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect('seller_view_product')
