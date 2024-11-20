from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from app.views import CustomLoginView
from app.forms import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
#path('custom_admin/', admin.site.urls),
    
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('service/',views.service,name='service'),
    path('blog/',views.blog,name='blog'),
    path('add_blog/',views.add_blog,name='add_blog'),
    path('blog/<int:id>/',views.full_blog,name='full_blog'),
    path('your_blog/',views.your_blog,name='your_blog'),
    path('contact/',views.contact,name='contact'),
    path('profile/', views.profile_section, name='profile_section'),  # View Profile
    path('profile/update/', views.update_profile, name='update_profile') , # Update Profile
  
    path('updatepost/<int:id>/',views.update_blog,name='updatepost'),
    path('delete/<int:id>/',views.delete_post,name='deletepost'),
    path('delete-account/', views.delete_account, name='delete_account'),
  


    path('accounts/login/', CustomLoginView.as_view(template_name='app/login.html'), name='login'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='signup'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),


    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),    

    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name="password_reset_complete"),




]