from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    pub_date=models.DateField()
    image=models.CharField(max_length = 400)

    def __str__(self) -> str:
        return self.product_name
    

class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default="")
    email=models.CharField(max_length=70,default="")
    phone=models.CharField(max_length=30 ,default="")
    desc=models.CharField(max_length=300,default="")
    

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json= models.CharField(max_length=5000)
    amount= models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    phone=models.CharField(max_length=20)

class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc=models.CharField(max_length=4000)
    time_Stamp=models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return self.update_desc[:7] + "..."