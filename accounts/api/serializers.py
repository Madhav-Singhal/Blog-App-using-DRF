from django.contrib.auth import get_user_model



from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )


User = get_user_model()


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]




class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
  
    password2 = CharField(label='Confirm password', write_only=True, style={'input_type': 'password',})
    password = CharField(label=' Password', write_only=True, style={'input_type': 'password',})

    class Meta:
        model = User
        fields = [
            'username',
            'email',
         
            'password',
            'password2'
            
        ]
        


    def validate(self, data):
    
        return data


    

    def validate_username(self, username):
        existing = User.objects.filter(username=username)
        if existing:
            raise ValidationError("Someone with that email address has already registered. Was it you?")

        return username



    def validate_email(self, email):
        existing = User.objects.filter(email=email).first()
        if existing:
            raise ValidationError("Someone with that email address has already registered. Was it you?")

        return email



    def validate_password(self, password):
        data = self.get_initial()
        
        password1 = data.get("password2")
        password2 = password
        if password1 != password2:
            raise ValidationError("passwords must match.")
        return password



    def validate_password2(self, password2):
        data = self.get_initial()
        password1 = data.get("password")
        password2 = password2
        if password1 != password2:
            raise ValidationError("passwords must match.")
        return password2



    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
                username = username,
                email = email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



class UserLoginSerializer(ModelSerializer):
    # token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    # email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields = [
            'username',
            # 'email',
            'password',
            # 'token',
            
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):
        user_obj = None
        username = data.get("username", None)
        password = data.get("password")

        user = User.objects.filter(username=username)
        user_obj=user.first()
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('does not match')
            
        return data

