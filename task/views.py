from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from task.models import Book, Cart, Category, WishList
from django.db.models import F
# Create your views here.

@csrf_exempt
def register(request):
    if not request.method == "POST":
        return JsonResponse({"status" : 400, "error": "Send a post request with valid parameters only."})
    username = request.POST["username"]
    email = request.POST["email"].lower()
    password = request.POST["password"]
    uname = User.objects.filter(username=username).first()
    em = User.objects.filter(email=email).first()
    try:
        if uname is None:
            if em is None:
                u=User(username=username,email = email)
                u.set_password(password)
                u.save()
                return JsonResponse({"user_id":u.id,"Status":"Account Created Successfully!"})
            else:
                return JsonResponse({"Status":"Email is already Registered!"})
        else:
            return JsonResponse({"Status":"Username is already Taken try another!"})
    except Exception as e:
        return JsonResponse({"400": str(e)})

def get_user_token(user):
    token_instance,  created = Token.objects.get_or_create(user=user)
    return token_instance.key

@csrf_exempt
def signin(request):
    if not request.method == "POST":
        return JsonResponse({"status" : 400, "error": "Send a post request with valid parameters only."})
        
    email = request.POST["email"].lower()
    password = request.POST["password"]
    try:
        user = User.objects.get(email=email)
        if user is None:
            return JsonResponse({ "status" : 400, "error": "There is no account with this email!"})
        if( user.check_password(password)):
            usr_dict = User.objects.filter(email=email).values().first()
            usr_dict.pop("password")
            if user != request.user:
                login(request, user)
                token = get_user_token(user)
                return JsonResponse({"status" : 200,"token": token,"status":"Logged in"})
            else:
                return JsonResponse({"status":200,"message":"User already logged in!"})
        else:
            return JsonResponse({"status":400,"status":"Invalid Login!"})
    except Exception as e:
        return JsonResponse({"400":"Invalid Login!"})

@csrf_exempt   
def signout(request):
    try:
        request.user.auth_token.delete()
        logout(request)
        return JsonResponse({ "status" : 200, "success" : "logout successful"})
    except User.DoeNotExist:
        return JsonResponse({ "status" : 400, "error": "Something Went wrong! Please try again later."})


class categoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        cname = request.POST["name"]
        c = Category(Name=cname)
        c.save()
        return JsonResponse({"status":200,"Message":"Category created!"})

    def get(self,request):
        cdata = Category.objects.values_list('Name',flat=True)
        return Response({"data":cdata})

class BookView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        bname = request.POST["name"]
        bauthor = request.POST["author"]
        bprice = request.POST["price"]
        cid = request.POST["category"]
        b=Book(Name=bname,author=bauthor,price=bprice)
        c = Category.objects.filter(id=cid).first()
        if c is not None:
            b.category = c
            b.save()
            return JsonResponse({"status":200,"Message":"Book is added!"})
        else:
            return JsonResponse({"status":404,"Message":"Category doesnot exist!"})

    def get(self,request,cid):
        bdata = Book.objects.filter(category__id=cid)
        proper_data = []
        d = dict()
        for i in bdata:
            d['id'] = i.id
            d['name'] = i.Name
            d['author'] = i.author
            d['price'] = i.price
            proper_data.append(d)
        return Response({"data":proper_data})

class cartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        user = request.user
        book_id = request.POST["book"]
        b = Book.objects.filter(id=book_id).first()
        c = Cart(book=b,customer=user)
        c.save()
        return JsonResponse({"status":200,"Message":"Added to cart!"})

    def get(self,request):
        d = Cart.objects.filter(customer=request.user).annotate(bid=F('book__id'),name=F('book__Name'),author=F('book__author'),price=F('book__price')).values('id','bid','name','author','price')
        return Response({"data":d})

    def delete(self,request,cid):
        b = Cart.objects.filter(id=cid).delete()
        return Response({"Message":"Removed from Cart!"})

class productView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        books = Book.objects.all()
        proper_data = []
        d = dict()
        for i in books:
            d['id'] = i.id
            d['name'] = i.Name
            d['author'] = i.author
            d['price'] = i.price
            proper_data.append(d)
        return Response({"data":proper_data})

class wishlistView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        user = request.user
        book_id = request.POST["book"]
        b = Book.objects.filter(id=book_id).first()
        c = WishList(book=b,customer=user)
        c.save()
        return JsonResponse({"status":200,"Message":"Added to Wishlsit!"})

    def get(self,request):
        d = WishList.objects.filter(customer=request.user).annotate(bid=F('book__id'),name=F('book__Name'),author=F('book__author'),price=F('book__price')).values('id','bid','name','author','price')
        return Response({"data":d})

    def delete(self,request,wid):
        b = WishList.objects.filter(id=wid).delete()
        return Response({"Message":"Removed from wishlist!"})