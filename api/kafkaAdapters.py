import json
import uuid
import time
import re

from kafka import KafkaProducer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthorizedUser
from api.serializers import PrescriptSerializer, DiagnosisSerializer


class IssueMessage(APIView):
    permission_classes([IsAuthorizedUser])
    diagnosis_serializer = DiagnosisSerializer
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
        # regex to match html opening and closing tags
        paragraph_array = []
        html_tag_regex = re.compile('(<p>(\w|\d|\n|\s|[\`\~\!\@\#\$\%\^\&\*' +
                                    '\(\)\-\_\=\+\\\|\[\]\{\}\;\:\'\"\,\.\<' +
                                    '\>\/\?])*?</p>)')
        reg = re.compile('(<.*?>)')
        for paragraph in html_tag_regex.finditer(emr_text):
            p = paragraph.group(0)
            for char in self.special_characters:
                p = p.replace(char, ' ' + char + ' ')
            p = reg.sub('', p)
            tokens = p.split()
            paragraph_array.append(tokens)

        # create a dft of the presracription
        try:
            request.data['id'] = int(uuid.uuid4().hex[0:15], 16)
            serializer = self.diagnosis_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.producer.send('hello.kafka', {
                'emr': paragraph_array,
                'uuid': request.data['id']
                # EMR식별자를 부여해서 uuid5를 사용할것 -> 중복방지
                # 'uuid': uuid.uuid5(uuid.NAMESPACE_URL, str(request.user))
            })
            self.producer.flush()

            # polling db for diagnosis result once per 1 second until the
            # diagnosis result is ready
            while True:
                diagnosis = self.diagnosis_serializer.Meta.model.objects.get(
                    id=request.data['id'])
                if diagnosis.named_entity:
                    new_text = ''
                    for idx, p in diagnosis.named_entity.items():
                        new_text += '<p>'
                        token_list = p['pr'] + p['te'] + p['tr']
                        # token_list.sort(key=lambda x: x['start'])

                        for i, ori in enumerate(paragraph_array[int(idx)]):
                            if token_list and \
                                    i in [x[0] for x in token_list]:
                                if i in [y[0] for y in p['pr']]:
                                    new_text += '<span class="pr">'
                                elif i in [y[0] for y in p['te']]:
                                    new_text += '<span class="te">'
                                elif i in [y[0] for y in p['tr']]:
                                    new_text += '<span class="tr">'

                            new_text += ori

                            if token_list and \
                                    i in [x[1] for x in token_list]:
                                new_text += '</span>'
                            new_text += ' '

                        new_text += '</p>'

                    return Response(new_text,
                                    status=status.HTTP_201_CREATED)
                else:
                    time.sleep(1)
