from rest_framework import serializers
from app.models import AddBlog,Profile,Contact,ContactInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.password_validation import validate_password

# Add blog
class AddBlogSerializer(serializers.ModelSerializer):
    class Meta:
        models = AddBlog
        fields = '__all__'

# Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'profile_pic', 'first_name', 'last_name', 'skills', 'bio']
        read_only_fields = ['user'] 

# Contact
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        models = Contact
        fields = '__all__'

# ContactInfo
class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        models = ContactInfo
        fields = '__all__'

# Signup
class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password1= serializers.CharField(write_only=True,style={'input_type':'password'})
    password2 = serializers.CharField(write_only=True,style={'input_type':'password'})

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    
    def validate(self,data):
        if data['password1']!=data['password2']:
            raise serializers.ValidationError({'password':'Password do not match'})
        return data
    
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email= validated_data['email'],
            password=validated_data['password1']
        )
        return user
    
# Login 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError(_('Invalid username or password'))
            elif not user.is_active:
                raise serializers.ValidationError(_('User account is disabled'))
            data['user'] = user
        else:
            raise serializers.ValidationError(_("Must include both 'username' and 'password'."))
        
        return data
    
# Change Password
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(wrtie_only=True)
    new_password2 = serializers.CharField(write_only=True)


    def validate(self,attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({'old_password':'The old password is incorrect.'})    
        
        if attrs['new_password1']!= attrs['new_password2']:
            raise serializers.ValidationError({'new_password2':'The new password do not match.'})
        
        validate_password(attrs['new_password1'],user=user)
        return attrs
    

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password1'])
        user.save()
        return user
    
# Password Reset 
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self,value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No account found with this emial"))
        return value
    
    def save(self):
        request = self.context.get('request')
        email = self.validate_data['email']
        reset_form = PasswordResetForm(data={'email':email})
        if reset_form.is_valid():
            reset_form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html'
            )


# Password Set Serializer
class PasswordSetSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self,attrs):
        user = self.get_user(attrs['uid'],attrs['token'])
        if not user:
            raise serializers.ValidationError(_('Invalid token or user ID.'))
        

        validate_password(attrs['new_password1'],user=user)
        return attrs
    
    def save(self):
        user = self.get_user(self.validated_data['uid'],self.validated_data['token'])
        user.set_password(self.validated_data['new_password1'])
        user.save()
        return user
    

    def get_user(self,uid,token):
        from django.utils.http import urlsafe_base64_decode
        from django.contrib.auth.tokens import default_token_generator

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except(TypeError,ValueError,OverflowError,User.DoesNotExist):
            return None
        
        if not default_token_generator.check_token(user,token):
            return None
        return user
