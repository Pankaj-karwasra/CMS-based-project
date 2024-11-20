from django.urls import path
from .views import AddBlogPostAPI, AddBlogGetAPI,AddBlogUpdateAPI,AddBlogDeleteAPI,ContactAPI, ContactInfoAPI,profile_section_api, update_profile_api,CustomerRegistrationView,LoginView,LogoutView,PasswordChangeView,PasswordResetView, PasswordSetView,DeleteView

urlpatterns = [
    path('blogs/', AddBlogGetAPI, name='blog-get'),
    path('blogs/add/', AddBlogPostAPI, name='blog-post'),
    path('blogs/update/<int:pk>/', AddBlogUpdateAPI, name='blog-update'),
    path('blogs/delete/<int:pk>/', AddBlogDeleteAPI, name='blog-delete'),
    path('register/', CustomerRegistrationView.as_view(), name='customer-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('contact/', ContactAPI, name='contact-api'),
    path('contact-info/', ContactInfoAPI, name='contact-info-api'),
    path('api/profile/', profile_section_api, name='profile-section-api'), 
    path('api/profile/update/', update_profile_api, name='update-profile-api'),
    path('api/password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('api/password-reset/',PasswordResetView.as_view(), name='password_reset'),
    path('api/password-reset-confirm/', PasswordSetView.as_view(), name='password_reset_confirm'),
    path('api/delete/',DeleteView,name='delete_account')





]
