from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status, filters, pagination
from rest_framework_jwt import authentication
from .serializers import AnswerSerializer, AnswerCreateSerializer, AnswerUpdateSerializer, TopAnswersSerializer
from answer.models import Answer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from notifications.signals import notify
from post.models import Post
from django.db.models import Count
from rest_framework.exceptions import NotFound
from django.core.paginator import InvalidPage
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from vote.models import AnswerVote

ANSWERS_PER_PAGE = 2


class AnswersPagination(pagination.PageNumberPagination):
    page_size = ANSWERS_PER_PAGE

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

    def paginate_queryset(self, queryset, request, view=None):
        """
        Overriding the method to get an entire page which a particular answer is belonged,
        as asked by the user in the query parameter 'answer'
        """
        answer_id = request.query_params.get('answer', None)
        post_belong = request.query_params.get('postBelong', None)

        '''here it calculates the corresponding page number where does the answer_id belong'''
        page_num = 1
        try:
            answers = queryset.filter(postBelong=post_belong)
            for index, answer in enumerate(answers):
                if str(answer.id) == str(answer_id):
                    page_num = index // ANSWERS_PER_PAGE + 1
                    # page_num = int(page_num)
        except Exception as exp:
            msg = 'For postBelong ' + str(exp) \
                  + ' Please enter a valid number or just remove the postBelong query parameter from the url'
            raise NotFound(msg)

        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, page_num)

        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)


class EntirePageByTheAnswerIdFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        answer_id = request.query_params.get('answer', None)
        post_belong = request.query_params.get('postBelong', None)

        answers = queryset.filter(postBelong=post_belong)
        print(answers)
        for index, answer in enumerate(answers):
            if str(answer.id) == str(answer_id):
                count = index / ANSWERS_PER_PAGE + 1
                print('count from filter:', int(count))
                # return queryset.filter(id=answer_id)
        return queryset.filter()


class AnswerViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    # queryset = Answer.objects.filter().annotate(vote_count=Count('answervote')).distinct()
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    pagination_class = AnswersPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'owner', 'postBelong']
    http_method_names = ['get']
    ordering_fields = ['up_vote_count', 'created_at', 'updated_at']

    def get_queryset(self):

        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        for obj in queryset:
            vote_count = AnswerVote.objects.filter(voteType='LIKE', answer=obj.id).count()
            obj.up_vote_count = vote_count
            obj.save(update_fields=['up_vote_count'])

        return queryset.order_by('-up_vote_count')


class AnswerCreateView(CreateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerCreateSerializer

    def create(self, request, *args, **kwargs):

        # print(to_user.notifications.unread())

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        obj = serializer.save()

        from_user = self.request.user
        action_object = Answer.objects.get(id=obj.id)
        message = from_user.username + ' has put an answer to your question'
        to_user = Post.objects.get(id=obj.postBelong.id).owner

        if from_user.is_authenticated and from_user != to_user:
            notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)

        serialized_obj = serializers.serialize('json', [obj, ])
        return serialized_obj


class AnswerUpdateView(UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data)

    def perform_update(self, serializer):
        obj = serializer.save()
        serialized_obj = serializers.serialize('json', [obj, ])
        return serialized_obj


class AnswerDeleteView(DestroyAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()

    def perform_destroy(self, instance):

        from_user = instance.owner
        action_object = instance
        to_user = instance.postBelong.owner
        content_type = ContentType.objects.get_for_model(Answer)
        ''' deleting comment notifications for the user '''
        notification = to_user.notifications.filter(actor_object_id=from_user.id,
                                                    action_object_content_type=content_type,
                                                    action_object_object_id=action_object.id)
        try:
            notification.delete()
        except Exception as excep:
            print(excep)

        instance.delete()


# Most voted answers
class TopAnswersViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.filter().annotate(vote_count=Count('answervote')).distinct()
    serializer_class = TopAnswersSerializer
    http_method_names = ['get']

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['vote_count']
