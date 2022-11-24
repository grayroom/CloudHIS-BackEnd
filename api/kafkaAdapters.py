import json

from kafka import KafkaProducer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthorizedUser


class IssueMessage(APIView):
    permission_classes([IsAuthorizedUser])
    # special_characters is a list of all ascii special character
    special_characters = [chr(i) for i in range(33, 48)] + \
                         [chr(i) for i in range(58, 65)] + \
                         [chr(i) for i in range(91, 97)] + \
                         [chr(i) for i in range(123, 127)]

    producer = KafkaProducer(bootstrap_servers=['192.168.0.13:9092'],
                             value_serializer=lambda x: json.dumps(x)
                             .encode('utf-8'))

    def post(self, request):
        emr_text = request.data['emr']
        # insert ' ' next to the special_characters in emr_text
        for char in self.special_characters:
            emr_text = emr_text.replace(char, ' ' + char + ' ')
        # split emr_text into a list of words
        emr_text = emr_text.split()

        self.producer.send('hello.kafka', {
            'emr': emr_text
        })
        self.producer.flush()
        return Response(status=status.HTTP_201_CREATED)
