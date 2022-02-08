from django.urls import path
from .import views

urlpatterns = [
    #register 
    path('register/',views.register,name='register'),
    #login
    path('signin/',views.signin,name='signin'),
    #logout
    path('signout/',views.signout,name='signout'),
    #add or get category names
    path('category/',views.categoryView.as_view(),name='categoryView'),
    #add book
    path('book/',views.BookView.as_view(),name='BookView'),
    #get books based on categories
    path('book/<int:cid>/',views.BookView.as_view(),name='BookView'),
    #add books to cart or get books in the cart
    path('cart',views.cartView.as_view(),name='cartView'),
    #remove book from cart
    path('cart/<int:cid>',views.cartView.as_view(),name='cartView'),
    #show all the produts
    path('product/',views.productView.as_view(),name='productView'),
    #add book to wishlist or get books from wishlist
    path('wishlist/',views.wishlistView.as_view(),name='wishlistView'),
    #remove books from wishlist
    path('wishlist/<int:wid>',views.wishlistView.as_view(),name='wishlistView')
]