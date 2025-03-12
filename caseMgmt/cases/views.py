from rest_framework.decorators import action
from .serializers import CaseSerializer, ServiceSerializer, CaseDocSerializer, ServDocSerializer
from .models import Case, Service, CaseDoc, ServDoc
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
import jieba.analyse


class CaseModelViewSet(ModelViewSet):
    serializer_class = CaseSerializer

    def get_queryset(self):
        return Case.objects.filter(supervisor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(supervisor=self.request.user)


class ServiceModelViewSet(ModelViewSet):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(case_belonged_id=self.kwargs['case_pk'])

    def perform_create(self, serializer):
        serializer.save(case_belonged_id=self.kwargs['case_pk'])


class UserKeywordsAPIView(APIView):
    def get(self, request):
        cases = Case.objects.filter(supervisor=self.request.user)

        content = ''
        for case in cases:
            content += case.case_name + '。'
        tags = jieba.analyse.extract_tags(content, topK=15, withWeight=True)
        keywords_list = []
        for tag in tags:
            keywords_list.append({'name': tag[0], 'value': int(tag[1] * 1000)})

        return Response(data=keywords_list)


class StatsAPIView(APIView):
    def get(self, request):
        cases = Case.objects.filter(supervisor=self.request.user)
        data = {
            'case_total': cases.count(),
            'case_in_progress': cases.filter(state=False).count(),
            'serv_total': 0,
            'serv_in_progress': 0
        }
        for case in cases:
            data['serv_total'] += Service.objects.filter(case_belonged=case).count()
            data['serv_in_progress'] += Service.objects.filter(case_belonged=case).filter(state=False).count()
        return Response(data=data)


class ServiceTypeStatsAPIView(APIView):
    def get(self, request):
        _dict = {
            '11': '科学研究与试验发展',
            '12': '专业化技术',
            '13': '科技推广及相关',
            '14': '科技信息',
            '15': '科技金融',
            '16': '科技普及和宣传教育',
            '17': '综合科技'
        }
        type_dict = {}
        cases = Case.objects.filter(supervisor=self.request.user)
        for case in cases:
            services = Service.objects.filter(case_belonged=case)
            for service in services:
                if service.type in type_dict:
                    type_dict[service.type] += 1
                else:
                    type_dict[service.type] = 1
        type_list = []
        for _type in type_dict:
            type_list.append({'name': _dict[_type], 'value': type_dict[_type]})

        return Response(data=type_list)


class CaseDocViewSet(ModelViewSet):
    serializer_class = CaseDocSerializer

    def get_queryset(self):
        case_id = self.request.query_params.get('case_id', None)
        if case_id is not None:
            return CaseDoc.objects.filter(case_belonged_id=case_id)
        return CaseDoc.objects.filter(case_belonged__supervisor=self.request.user)

    @action(methods=['get'], detail=True)
    def download(self, request, *args, **kwargs):
        file_obj = self.get_object()
        response = FileResponse(open(file_obj.file.path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment; filename={}".format(str(file_obj.file).split('/')[-1]
                                                                           .encode('utf-8').decode('iso-8859-1'))
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response


class ServDocViewSet(ModelViewSet):
    serializer_class = ServDocSerializer

    def get_queryset(self):
        serv_id = self.request.query_params.get('serv_id', None)
        if serv_id is not None:
            return ServDoc.objects.filter(serv_belonged_id=serv_id)
        return ServDoc.objects.filter(serv_belonged__case_belonged__supervisor=self.request.user)

    @action(methods=['get'], detail=True)
    def download(self, request, *args, **kwargs):
        file_obj = self.get_object()
        response = FileResponse(open(file_obj.file.path, 'rb'))
        response['Content-Type'] = 'application/octet-stream; charset=utf-8'
        response['Content-Disposition'] = "attachment; filename={}".format(str(file_obj.file).split('/')[-1])
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response
