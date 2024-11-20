from django.shortcuts import render
from django.contrib.auth import login,logout
from .serializer import CustomerRegistrationSerializer,LoginSerializer,ContactSerializer,ContactInfoSerializer,ProfileSerializer,AddBlogSerializer, PasswordChangeSerializer,PasswordResetSerializer,PasswordSetSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from app.models import AddBlog,Profile,Contact,ContactInfo
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash


# Add blog POST api
@api_view(['POST'])
def AddBlogPostAPI(request):
    if request.method =='POST':
        serializer = AddBlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Add Blog Successfully','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'error':serializer.errors},status=status.HTTP_404_NOT_FOUND)
    

# Add blog GET api
@api_view(['GET'])
def AddBlogGetAPI(request):
    if request.method == 'GET':
        blog = AddBlog.objects.all()
        serializer = AddBlogSerializer(blog,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Get Blog Successfully','data':serializer.data},status=status.HTTP_202_ACCEPTED)
    return Response({'error':serializer.errors},status=status.HTTP_404_NOT_FOUND)


# Update Blog api
@api_view(['PUT','PATCH'])
def AddBlogUpdateAPI(request,pk):
    try:
        blog = AddBlog.objects.get(pk=pk)
    except AddBlog.DoesNotExist:
        return Response({'error':'Blog Not found'},status=status.HTTP_404_NOT_FOUND)
    
    if request.method in['PUT','PATCH']:
        serializer = AddBlogSerializer(blog,data=request.data,partial=(request.method=='PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Blog Updated Successfully','data':serializer.data},status=status.HTTP_200_OK)
        return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

# Delete Blog Api
@api_view(['DELETE'])
def AddBlogDeleteAPI(request,pk):
    try:
        blog = AddBlog.objects.get(pk=pk)
    except AddBlog.DoesNotExist:
        return Response({'error':'Blog Not Found'},status=status.HTTP_404_NOT_FOUND)
    blog.delete() 
    return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Contact API
@api_view(['POST'])
def ContactAPI(request):
    serializer = ContactSerializer(data=request.data)  
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Team will contact you soon!', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Contact Info API
@api_view(['GET'])
def ContactInfoAPI(request):
    info = ContactInfo.objects.all()
    serializer = ContactInfoSerializer(info, many=True)  
    return Response(
        {'message': 'Contact info fetched successfully!', 'data': serializer.data},
        status=status.HTTP_200_OK
    )

# Profile API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_section_api(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({'error':'Profile not fouond for the user'},status=status.HTTP_400_BAD_REQUEST)
    
    serializer = ProfileSerializer(profile)
    return Response({'data':serializer.data},status=200)

# Update Profile
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile_api(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({'error':'Profile not found for the user'},status=status.HTTP_400_BAD_REQUEST)
    
    serializer = ProfileSerializer(profile,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'Profile updated successfully','data':serializer.data},status=status.HTTP_200_OK)
    return Response({'error': serializer.errors}, status=400)

    


# Signu API
class CustomerRegistrationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User registered successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    

# Login API
class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request,user)
            return Response({'message':'Login successfull'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# Logout API
class LogoutView(APIView):
    def post(self,request,*args,**kwargs):
        logout(request)
        return Response({'message':'You have successfully logged out'},status=status.HTTP_404_NOT_FOUND)
    

# Password Change API
class PasswordChangeView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = PasswordChangeSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            update_session_auth_hash(request,request.user)
            return Response({'message':'Password change successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# Password Reset API
class PasswordRestView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = PasswordResetSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Password reset email has been sent'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# Password Set API
class PasswordSetView(APIView):
    def post(self,request,*args,**kwargs):
        serializer = PasswordSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Password has been reset successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



# Delete Account
class DeleteView(APIView):
    def post(self,request,*args,**kwargs):
        user = request.user
        if user.is_authenticated:
            user.delete()
            logout(request)
            return Response({'message':'Account deleted Successfully'},status=status.HTTP_200_OK)
        else:   
            return Response({'message':'Unatheorized user'},status=status.HTTP_401_UNAUTHORIZED)