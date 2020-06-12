from django.db.models import Q
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
    )

from rest_framework.generics import (

    ListAPIView, 
    RetrieveAPIView, 
    UpdateAPIView, 
    DestroyAPIView, 
    CreateAPIView,
    RetrieveUpdateAPIView
)


from rest_framework.pagination import (

    LimitOffsetPagination,
    PageNumberPagination,
    )

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination


from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    # IsOwnerOfObject

)

from rest_framework.response import Response
from rest_framework.reverse import reverse


from .permissions import IsOwnerOrReadOnly

from blogapp.models import Base, AddComment

from .serializers import (
    PostListSerializer, 
    PostCreateUpdateSerializer, 
    PostDetailSerializer,
    CommentSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    create_comment_serializer
)

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin, CreateModelMixin

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.renderers import TemplateHTMLRenderer


class PostCreateView(CreateAPIView):
    queryset = Base.objects.all()
    serializer_class = PostCreateUpdateSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)




class PostListView(CreateModelMixin, ListAPIView): 
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'rest_framework/x.html'
    
   

    def get_queryset(self, *args, **kwargs):
        queryset_list = Base.objects.all()

        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains= query)

                ).distinct()

        return queryset_list
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# class PostListView(ListAPIView):
#     # queryset_list = Base.objects.all()
    
#     serializer_class = PostListSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fields = ['title'] #used to search according to title field mention in models 

#     pagination_class = PostPageNumberPagination
#     permission_classes = [AllowAny]


#     def get_queryset(self, *args, **kwargs):
#         queryset_list = Base.objects.all()
#         query = self.request.GET.get("q")
#         if query:
#             queryset_list = queryset_list.filter(
#                 # Q(add_title__icontains = query) |
#                 Q(title__icontains= query)

#                 ).distinct()

    

#         return queryset_list

















class PostDetailView(RetrieveAPIView):
    queryset = Base.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'
    permission_classes = [AllowAny]




class PostUpdateView(RetrieveUpdateAPIView):
    queryset = Base.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwnerOrReadOnly]

   
    def perform_update(self, serializer):
        serializer.save(user = self.request.user)




class PostDeleteView(DestroyAPIView):
    queryset = Base.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwnerOrReadOnly]





class CommentDetailView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = AddComment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]


    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




class CommentListView(ListAPIView):
    
    serializer_class = CommentListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['comment'] 

    pagination_class = PostPageNumberPagination



    def get_queryset(self, *args, **kwargs):
        queryset_list = AddComment.objects.filter(id__gte=0) #filter(user=self.request.user)
        # queryset_list = AddComment.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(comment__icontains = query) 
                # Q(user__first_name__icontains= query)

                ).distinct()

        return queryset_list



class CommentCreateView(CreateAPIView):
    queryset = AddComment.objects.all()
    
    

    def get_serializer_class(self):
        pk = self.kwargs.get('pk')

        cmnt = Base.objects.get(pk=pk)
        parent_id = self.kwargs.get('parent_id')

       
        return create_comment_serializer(
                post_id=cmnt,
                parent_id=parent_id,
                user=self.request.user
                )