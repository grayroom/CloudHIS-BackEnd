import json
import uuid
import time
import re
import environ

from kafka import KafkaProducer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


from api.permissions import IsAuthorizedUser
from api.serializers import PrescriptSerializer, DiagnosisSerializer, NerHistorySerializer

from config import settings
import jwt


env = environ.Env()
environ.Env.read_env()


class IssueMessage(APIView):
    permission_classes([IsAuthorizedUser])
    ner_serializer = NerHistorySerializer
    # special_characters is a list of all ascii special character
    special_characters = [chr(i) for i in range(33, 48)] + \
                         [chr(i) for i in range(58, 65)] + \
                         [chr(i) for i in range(91, 97)] + \
                         [chr(i) for i in range(123, 127)]

    html_tag_regex = re.compile('(<p>(\w|\d|\n|\s|[\`\~\!\@\#\$\%\^\&\*' +
                                '\(\)\-\_\=\+\\\|\[\]\{\}\;\:\'\"\,\.\<' +
                                '\>\/\?])*?</p>)')
    reg = re.compile('(<.*?>)')

    producer = KafkaProducer(bootstrap_servers=[env("KAFKA_HOST") + ":" + env("KAFKA_PORT")],
                             value_serializer=lambda x: json.dumps(x)
                             .encode('utf-8'))

    def post(self, request):
        target_emr_array = [
            {
                'uuid': int(uuid.uuid4().hex[0:15], 16),
                'text': request.data['preliminary'],
                'token_list': [],
                'html': "",
                'ner_result': {},
                'key_factor_list': [],
                'updated_time': ""
            },
            {
                'uuid': int(uuid.uuid4().hex[0:15], 16),
                'text': request.data['comment'],
                'token_list': [],
                'html': "",
                'ner_result': {},
                'key_factor_list': [],
                'updated_time': ""
            }
        ]

        for emr in target_emr_array:
            for paragraph in self.html_tag_regex.finditer(emr['text']):
                p = paragraph.group(0)
                for char in self.special_characters:
                    p = p.replace(char, ' ' + char + ' ')
                p = self.reg.sub('', p)
                tokens = p.split()
                emr['token_list'].append(tokens)
            # create a draft of the presracription
            try:
                self.ner_serializer = NerHistorySerializer(data={
                    'id': emr['uuid'],
                    'target_text': emr['text'],
                    'paitent_id': request.data['patient_id'],
                    'doctor_id': get_payload(request)['user_id'],
                })
                if self.ner_serializer.is_valid():
                    self.ner_serializer.save()
                else:
                    return Response(self.ner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
            else:
                emr['updated_time'] = self.ner_serializer.Meta.model.objects.get(
                    id=emr['uuid']).updated_time
                self.producer.send('hello.kafka', {
                    'emr': emr['token_list'],
                    'uuid': emr['uuid']
                })

        # NOTE: diagnosis.comment에 개체명이 인식완료되면 Response를 보내준다.
        # polling하는 로직이 좀 구리다

        while self.ner_serializer.Meta.model.objects.get(
                id=target_emr_array[0]['uuid']).updated_time == target_emr_array[0]['updated_time'] or \
            self.ner_serializer.Meta.model.objects.get(
                id=target_emr_array[1]['uuid']).updated_time == target_emr_array[1]['updated_time']:
            time.sleep(1)

        temp_res = self.ner_serializer.Meta.model.objects.get(
            id=target_emr_array[0]['uuid'])
        target_emr_array[0]['updated_time'] = temp_res.updated_time
        target_emr_array[0]['ner_result'] = temp_res.ner_result
        temp_res = self.ner_serializer.Meta.model.objects.get(
            id=target_emr_array[1]['uuid'])
        target_emr_array[1]['updated_time'] = temp_res.updated_time
        target_emr_array[1]['ner_result'] = temp_res.ner_result

        for emr in target_emr_array:
            new_text = ''
            key_factor_list = {
                "pr": [],
                "te": [],
                "tr": []
            }
            temporal_keyword = ""
            tag_flag = ""

            if emr['ner_result'] == {}:
                emr['html'] = emr['text']
                continue
            for idx, p in emr['ner_result'].items():
                new_text += '<p>'
                token_list = p['pr'] + p['te'] + p['tr']

                for i, ori in enumerate(emr['token_list'][int(idx)]):
                    # NOTE: 개체명 인식 pair에 대해서 span tag를 추가한다. x[0]은 시작, x[1]은 끝
                    if token_list and i in [x[0] for x in token_list]:
                        temporal_keyword = ""  # temporal_keyword 초기화
                        if i in [y[0] for y in p['pr']]:
                            new_text += '<span class="pr">'
                            tag_flag = "pr"
                        elif i in [y[0] for y in p['te']]:
                            new_text += '<span class="te">'
                            tag_flag = "te"
                        elif i in [y[0] for y in p['tr']]:
                            new_text += '<span class="tr">'
                            tag_flag = "tr"

                    temporal_keyword += ori + ' '
                    new_text += ori + ' '

                    if token_list and i in [x[1] for x in token_list]:
                        if tag_flag == "pr":
                            key_factor_list['pr'].append(temporal_keyword)
                        elif tag_flag == "te":
                            key_factor_list['te'].append(temporal_keyword)
                        elif tag_flag == "tr":
                            key_factor_list['tr'].append(temporal_keyword)
                            new_text += '</span>'

                new_text += '</p>'

            emr['html'] = new_text
            emr['key_factor_list'] = key_factor_list

        return Response({
            json.dumps(target_emr_array, default=str)
        }, status=status.HTTP_201_CREATED)


def get_payload(req):
    token = req.headers.get("Authorization", None)
    access_token = token.split(" ")[1]
    return jwt.decode(access_token,
                      settings.SIMPLE_JWT['VERIFYING_KEY'],
                      algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
