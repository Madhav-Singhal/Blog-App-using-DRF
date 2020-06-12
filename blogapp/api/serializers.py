from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    CharField
    )


from blogapp.models import Base, AddComment
from accounts.api.serializers import UserDetailSerializer





class PostCreateUpdateSerializer(ModelSerializer):

    
    class Meta:
        model = Base
        fields = [ 'title', 'body']



class PostListSerializer(ModelSerializer):

    detail_url = HyperlinkedIdentityField(
        view_name = 'blogs-api:detail', 
        lookup_field = 'pk'
        )

    

    # createpost = SerializerMethodField()

    user = SerializerMethodField()
    # def get_createpost(self, obj):
        

    #     return self.context['request'].build_absolute_uri(obj.get_url())


    class Meta:
        model = Base

        fields = [ 'user', 'title', 'body', 'detail_url'] #. 'delete_url'

     

    def get_user(self, obj):

        return obj.user.username



    
class PostDetailSerializer(ModelSerializer):
    createcmnts = HyperlinkedIdentityField(
        view_name = 'blogs-api:c-create', 
        lookup_field = 'pk'
        )
    edit_url = HyperlinkedIdentityField(
        view_name = 'blogs-api:edit', 
        lookup_field = 'pk'
        )
    user = UserDetailSerializer(read_only=True)
 
    comments = SerializerMethodField()


    class Meta:
        model = Base
        fields = [ 'createcmnts', 'title', 'body', 'user', 'edit_url', 'comments']


    def get_comments(self, obj):
        
        post_id = obj.id
        c_qs = AddComment.objects.filter(post_id=post_id).filter(parent=None)
        content = CommentSerializer(c_qs, many = True, context=self.context).data
        return content




class CommentSerializer(ModelSerializer):
    cmnt_detail_url = HyperlinkedIdentityField(
        view_name = 'blogs-api:c-detail', 
        lookup_field = 'pk'
        )
    user = SerializerMethodField()
    post_title = SerializerMethodField()

    reply_url = SerializerMethodField()
    reply_count = SerializerMethodField()
    class Meta:
        model = AddComment
        fields = ['reply_url', 'user', 'post_title', 'comment','reply_count', 'cmnt_detail_url']

    def get_reply_count(self, obj):

        if obj.is_parent:
            return obj.children().count()
        return 0


    def get_reply_url(self, obj):
        

        return self.context['request'].build_absolute_uri( obj.get_api_url())


    def get_user(self, obj):
        return obj.user.username

    def get_post_title(self, obj):
        
        x = Base.objects.filter(id=obj.post_id_id).values_list('title', flat=True).first()
        return x










def create_comment_serializer(post_id=None, user=None, parent_id=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = AddComment
            fields = [
                'id',
                'comment'
            ]
        

        def __init__(self, *args, **kwargs):
            
            self.parent_obj = None
            if parent_id:
                parent_qs = AddComment.objects.filter(id=parent_id)

                if parent_qs.exists() and parent_qs.count() ==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)
    
        def create(self, validated_data):
            content = validated_data.get("comment")
            
            parent_obj = self.parent_obj

            comment = AddComment.objects.create(
                    post_id=post_id,
                    user=user,
                    comment = content,
                    parent=parent_obj
                    )
            return comment

    return CommentCreateSerializer





class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='blogs-api:c-detail')
    reply_count = SerializerMethodField()
    class Meta:
        model = AddComment
        fields = [
            'url',
            'id',
           
            'comment',
            'reply_count',
            
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0








class CommentChildSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only = True)
    class Meta:
        model = AddComment
        fields = [
        
            
            'user',
            'comment',

        ]


class CommentDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only = True)
    reply_count = SerializerMethodField()
    replies =   SerializerMethodField()
    class Meta:
        model = AddComment
        fields = [
            
            'user',
            
            'comment',
            'reply_count',
            'replies',
            
        ]
        read_only_fields = [
            
            'reply_count',
            'replies',
           
        ]

    
    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

