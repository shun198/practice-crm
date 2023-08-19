# from application.injectors import injector
from application.injectors.sns import sns_injector
from application.serializers.sns import SnsSerializer
from application.utils.sns import SnsWrapper
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class SnsViewSet(ViewSet):
    """SMS関連のViewSet"""

    serializer_class = SnsSerializer
    permission_classes = [AllowAny]

    @action(methods=["post"], detail=False)
    def sns(self, request):
        """SMSの送信処理"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        sns = sns_injector.get(SnsWrapper)
        message_id = sns.publish_text_message(
            "+81" + serializer.validated_data["phone_number"],
            serializer.validated_data["message"],
        )
        return Response({"message_id": message_id}, status=status.HTTP_200_OK)
