from django.urls.conf import path
from rest_framework.schemas.coreapi import ManualSchema
from rest_framework.views import APIView
from myapi.serializers import DeleteManySerializer, HeroSerializer, PasswordSerializer
from myapi.models import Hero
from django.shortcuts import get_list_or_404, get_object_or_404, render
from rest_framework import viewsets, status, filters
from rest_framework.authentication import BaseAuthentication, BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, schema
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filterset
import coreapi
import coreschema
from rest_framework.schemas import AutoSchema
import django_filters

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 1000


class HeroFilterSet(django_filters.FilterSet):
    ids = django_filters.BaseCSVFilter(
        field_name='id',
        lookup_expr='in', help_text="csv列表, 如: 1,2,3")

    class Meta:
        model = Hero
        fields = ['ids']


class HeroViewSet(viewsets.ModelViewSet):
    """
    create:
    创建项目

    retrieve:
    获取项目详情数据

    update:
    完整更新项目

    partial_update:
    部分更新项目

    destroy:
    删除项目

    list:
    获取项目列表数据
    """
    ordering = ['id']
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = ['name', 'alias']

    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'post', 'delete'], schema=AutoSchema([
        coreapi.Field(
            'ids',
            required=True,
            location='query',
            schema=coreschema.String(
                description='csv列表, 如: 1,2,3'
            )
        ),
    ]))
    def many(self, request):
        """
        get:
        批量获取
        post:
        批量更新
        delete:
        批量删除
        """

        ids = request.query_params.get('ids', '')
        ids = {x.strip() for x in ids.split(',') if x.strip().isdigit()}
        list = Hero.objects.filter(id__in=ids)
        if request.method == 'GET':
            serializer = self.get_serializer(list, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            list.update(**serializer.data)
            serializer = self.get_serializer(list, many=True)
            return Response(serializer.data)
        else:
            list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], serializer_class=PasswordSerializer)
    def set_password(self, request, pk=None):
        '''
        设置密码
        '''

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
        # serializer = PasswordSerializer(data=request.data)
        # if serializer.is_valid():
        # else:
        #     return Response(serializer.errors,
        #                     status=status.HTTP_400_BAD_REQUEST)


# class HeroView(APIView):
#     ordering = ['id']
#     queryset = Hero.objects.all()
#     serializer_class = HeroSerializer
#     filter_backends = [DjangoFilterBackend, ]
#     filterset_class = HeroFilterSet

#     def get(self, request):
#         queryset = self.filter_queryset(self.get_queryset())
#         ids = self.request.query_params.get('ids', None)
#         if ids is not None:
#             ids_list = ids.split(',')
#             queryset = queryset.filter(id__in=ids_list)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
