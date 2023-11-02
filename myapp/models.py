from django.db import models

# Create your models here.
class User(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField()
    mobile=models.PositiveIntegerField()
    address=models.TextField()
    password=models.CharField(max_length=100)
    profile_pic=models.ImageField(upload_to="profile_pic/",default="")
    usertype=models.CharField(max_length=100,default="buyer")

    def __str__(self):
        return self.fname+" "+self.lname
    
class Product(models.Model):
    seller=models.ForeignKey(User,on_delete=models.CASCADE)
    choice1=(
        ("Laptop","Laptop"),
        ("Accessories","Accessories"),
        ("Camera","Camera"),
    )
    product_category=models.CharField(max_length=100,choices=choice1)
    product_name=models.CharField(max_length=100)
    product_price=models.PositiveIntegerField()
    product_desc=models.TextField()
    product_image=models.ImageField(upload_to="product_image")

    def __str__(self):
        return self.seller.fname+" - "+self.product_name
