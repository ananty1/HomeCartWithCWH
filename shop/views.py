from django.shortcuts import render,redirect
from .models import Product,Contact,Order,OrderUpdate
from django.http import HttpResponse
from math import ceil
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from payTm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';
# Create your views here.

def index(request):
    allprod=[]
    categprod=Product.objects.values('category','id')
    categs={item['category'] for item in categprod}
    for categ in categs:
        prod=Product.objects.filter(category=categ)
        n=len(prod)
        numslides=(n//4)+ ceil(n/4-(n//4))
        if n!=0:
            allprod.append([prod,range(1,numslides),numslides])
    params={'allprod':allprod}
    return render(request,'shop/index.html',params)

def searchMatch(query,item):
    if query in item.product_name.lower() or query in item.desc.lower() or query in item.category.lower():
        print("Found")
        return True
    else:
        return False



def search(request):
    query=request.GET.get('search')
    allprod=[]
    categprod=Product.objects.values('category','id')
    categs={item['category'] for item in categprod}
    for categ in categs:
        prodtemp=Product.objects.filter(category=categ)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        numslides=(n//4)+ ceil(n/4-(n//4))
        if n!=0:
            allprod.append([prod,range(1,numslides),numslides])
    params={'allprod':allprod,'msg':""}
    if len(allprod)==0 or len(query)<4:
        params={'msg':'Please make sure to enter the relevant search query and length of query should be greater than 4'}
        

    return render(request,'shop/search.html',params)

def about(request):
    return render(request,'shop/about.html')


def contact(request):
    thank=False
    if request.method=='POST':
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        print(name,email,phone,desc)
        contact=Contact(name=name, email=email, phone=phone, desc=desc)
        thank=True
        contact.save()
        return render(request,'shop/contact.html',{"thank":thank})
    return render(request,'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    str_date = str(item.time_Stamp)
                    date = datetime.date( int(str_date[:4]),  int(str_date[5:7]),  int(str_date[8:]) )
                    time = date.ctime()
                    print(time)
                    updates.append({'text': item.update_desc, 'time': time[:3] + ", " + time[4:10] + " " + time[-4:]})
                    response = json.dumps({"status":"success", "updates":updates,"itemjson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"noitem"}')

    return render(request, 'shop/tracker.html')




def productView(request,myid):
    # Fetch the product by id
    product=Product.objects.filter(id=myid)[0]
    # print(product)
    return render(request,'shop/prodView.html',{'product':product})


def checkout(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        itemsjson=request.POST.get('itemsjson','')
        amount=request.POST.get('amount','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','') +" "+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        print(name,email,phone)
        order=Order(items_json=itemsjson ,amount=amount,name=name, email=email,address=address,city=city,state=state,zip_code=zip_code, phone=phone,)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="The order has been placed.")
        update.save()
        thank=True
        id=order.order_id 
        # return render(request,'shop/checkout.html',{'thank':thank,'id':id})
        # request paytm to transfer to your account after payment by user 
        param_dict={
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlepayment/',#paytm will tell us the confirmation.
        }
        param_dict['CHECKSUMHASH']= Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'shop/paytm.html',{'param_dict':param_dict})
    return render(request,'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    #paytm will send us post request here.
    form=request.POST()
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            checksum=form[i]
    verify= Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE']=='01':
            print('Order Successful')
        else:
            print('Order is not successful because ',response_dict['RESPMSG'])
             
    return render(request,'shop/paymentstatus.html',{'response':response_dict})


