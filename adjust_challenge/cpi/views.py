from django.db import models
from django.db.models import Sum
from django.db.models.expressions import F, ExpressionWrapper
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .models import ADCampaigns, ADCampSerializer


class EmptyParams(Exception):
    pass


class NotValidParams(Exception):
    pass


def validate_params(request, fields, queryparam):
    """
     This method is to validate the parameters send by Client
    :param request: request object
    :param fields: the applicable feilds
    :param queryparam: Name of the queryparam
    :return: cleaned params or raise an exception
    """
    params = request.query_params.get(queryparam)
    if params:
        params = [param.strip().lower() for param in params.split(',')]
        if all([param in fields for param in params]):
            return params
        else:
            invalid_params =  set(params) - set(fields)
            raise NotValidParams(f"{''.join(invalid_params)}")
    else:
        raise EmptyParams("Params not Provided!")


class ADCampaignList(generics.ListAPIView):
    """
    This a generic View to display the AD Campaign Results
    """
    queryset = ADCampaigns.objects.all()
    serializer_class = ADCampSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'date': ['gte', 'lte', 'exact', 'gt', 'lt'],
        'channel': ['exact'],
        'country': ['exact'],
        'os': ['exact'],
    }
    groupby_feilds = ['date', 'channel', 'country', 'os']
    column_fields = ['impressions', 'clicks', 'installs', 'spend', 'revenue', 'cpi']
    ordering_fields = groupby_feilds + column_fields

    def filter_data(self):
        """
        filters the data according to the filter applied by user
        :return: queryset
        """
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        return queryset

    def group_data(self, request, queryset):
        """
        Validates and groups the data
        :param request: request of user
        :param queryset: filtered queryset
        :return: grouped queryset
        """
        groupby_params = validate_params(request, self.groupby_feilds, 'groupby')
        if groupby_params:
            return queryset.values(*groupby_params).order_by(*groupby_params)
        else:
            raise NotValidParams("Not a Valid groupby Column!")

    def ordering_data(self, request, queryset):
        """
         Validates and orders the data
        :param request: request of user
        :param queryset: annotated queryset
        :return: querset with ordering
        """

        # both ascending and descending params
        ordering_feilds = self.ordering_fields + [f'-{i}' for i in self.ordering_fields]
        try:
            ordering_params = validate_params(request, ordering_feilds, 'ordering')
        except EmptyParams:
            return queryset
        if ordering_params:
            return queryset.order_by(*ordering_params)
        else:
            raise NotValidParams("Not a Valid ordering Column!")

    def columns_to_include(self, request, queryset):
        """
         validates and includes columns specified by user
        :param request: request of user
        :param queryset: grouped queryset
        :return: annotated queryset
        """
        try:
            column_parms = validate_params(request, self.column_fields, 'columns')
        except EmptyParams:
            column_parms = self.column_fields

        if 'cpi' in column_parms:
            column_parms.remove('cpi')
            column_parms = {columnname: Sum(columnname) for columnname in column_parms}
            spend = F('spend') if 'spend' in column_parms else Sum('spend')
            installs = F('installs') if 'installs' in column_parms else Sum('installs')
            column_parms['cpi'] = ExpressionWrapper(spend / installs, output_field=models.FloatField())
            return queryset.annotate(**column_parms)
        elif column_parms:
            column_parms = {columnname: Sum(columnname) for columnname in column_parms}
            return queryset.annotate(**column_parms)
        else:
            raise NotValidParams("Not a Valid Column!")

    def list(self, request, *args, **kwargs):

        # 1 filter the data
        queryset = self.filter_data()

        # 2 group the data
        try:
            grouped_qs = self.group_data(request, queryset)
        except EmptyParams:
            return Response(
                {"message": f"Please provide atleast one groupby columns from : {','.join(self.groupby_feilds)}"},
                status=status.HTTP_400_BAD_REQUEST)
        except NotValidParams as nvp:
            return Response({"message": f" Invalid Groupby parm :{nvp}, You can choose from these : {','.join(self.groupby_feilds)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # 3 add column aggregation to the data
        try:
            columns_data = self.columns_to_include(request, grouped_qs)
        except NotValidParams as nvp:
            return Response({"message": f"Invalid Column parm {nvp}, You can choose from these : {','.join(self.column_fields)}"},
                            status=status.HTTP_400_BAD_REQUEST)
        # 3 ordering the data
        try:
            ordered_data = self.ordering_data(request, columns_data)
        except NotValidParams as nvp:
            return Response(
                {"message": f"Invalid Ordering param {nvp}, You can choose from these : {','.join(self.ordering_fields)}"},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(ordered_data, status=status.HTTP_200_OK)
