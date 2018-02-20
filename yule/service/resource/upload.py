# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import upyun
import logging
import traceback
import ujson as json
from datetime import date
from itertools import chain
from diyidan.database.model.image_info import ImageInfoModel
from diyidan.lib import utils
from diyidan.lib.service import Service
from diyidan.lib.singleton import singleton
from diyidan.service.constants.other import JSON_DICT_FMT
from diyidan.service.constants.other import JSON_STR_FMT
from diyidan.service.constants.other import OBJ_ATTR_FMT
from diyidan.database.redis_key.redis_pika import resource
from qiniu import Auth
from base64 import urlsafe_b64encode
from tornado import gen
from tornado import httpclient
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest

qiniu_auth = Auth('f1VWrxM4102vhPMIC_lXGVcrYy6W2o__kLpURvWU', 'phr1yVPJ1-0ZyOhEbbmyN2paH2rC0AYo6qPc_bYH')


@singleton
class UploadService(Service):
    def get_upload_token(self, host):
        policy = {
            'callbackUrl': 'http://' + host + '/v0.2/upyun',
            'callbackBody': 'image-width=$(imageInfo.width)&image-height=$(imageInfo.height)&image-type=$(imageInfo.format)&url=$(key)&image-source=qiniu'
        }
        token = qiniu_auth.upload_token('diyidan', None, 86400, policy)
        token_music = qiniu_auth.upload_token('diyidan-music', None, 86400, None)
        policy_chat = {
            'callbackUrl': 'http://' + host + '/v0.2/upyun',
            'callbackBody': 'image-width=$(imageInfo.width)&image-height=$(imageInfo.height)&image-type=$(imageInfo.format)&url=$(key)&image-source=qiniu&image-usage=chat'
        }

        token_chat = qiniu_auth.upload_token('diyidan-chat', None, 86400, policy_chat)
        data = {
            'key': '/W8f7EPgIa0YZIz8w6jjMQkW0B4=',
            'musicKey': 'JkVt2fOi3OJWUwsLZ5jLClxMOH4=',
            'chatKey': 'Cw4CPKnB31vq0GLB+QV23iFWV+U=',
            'qiniuToken': token,
            'qiniuTokenMusic': token_music,
            'qiniuTokenChat': token_chat,
        }

        return data

    @gen.coroutine
    def upload_image_to_upyun_by_image_url(self, source_image_url, upload_category='default'):
        """
        :param source_image_url:
        :param upload_category:
        :return: None means Failed, not None is the upload result
        """

        http_client = AsyncHTTPClient(max_clients=125)

        today = date.today()
        image_upload_short_url = '/' + upload_category + '/' + str(today.year) + '/' + str(today.month) + '/' + str(
            today.day) + '/' + utils.my_random_string(16) + '.jpg'

        upload_result_flag = False
        try:
            # try to use upyun self-fetch api upload image
            target_url = 'diyidan:' + image_upload_short_url[1:]
            source_url = source_image_url
            source_url = urlsafe_b64encode(source_url)
            target_url = urlsafe_b64encode(target_url)
            fetch_url = 'http://iovip.qbox.me/fetch/{source_url}/to/{target_url}'.format(source_url=source_url,
                                                                                         target_url=target_url)

            auth_code = qiniu_auth.token_of_request(fetch_url)
            headers = {"Content-Type": 'application/x-www-form-urlencoded', 'Authorization': 'QBox ' + auth_code}

            request = HTTPRequest(fetch_url, "POST", headers=headers, body='', allow_ipv6=False)

            res = yield http_client.fetch(request)
            response = json.loads(res.body)

            if 'key' in response and response['key'] == image_upload_short_url[1:]:
                upload_result_flag = True

        except Exception as e:
            logging.warning("Error: " + str(e))

        if not upload_result_flag:
            try:
                # try get local first then upload local image to upyun
                responses = yield http_client.fetch(source_image_url, allow_ipv6=False)

                policy = {'callbackUrl': 'http://api.diyidan.net/v0.2/upyun',
                          'callbackBody': 'image-width=$(imageInfo.width)&image-height=$(imageInfo.height)&image-type=$(imageInfo.format)&url=$(key)&image-source=qiniu'}

                token = qiniu_auth.upload_token('diyidan', None, 120, None)
                fields = [('token', token), ('key', image_upload_short_url[1:])]
                files = [('file', 'file', responses.body)]

                content_type, body = utils.encode_multipart_formdata(fields, files)
                headers = {"Content-Type": content_type, 'content-length': str(len(body))}
                request = HTTPRequest("http://up.qbox.me", "POST", headers=headers, body=body, allow_ipv6=False)

                res = yield http_client.fetch(request)
                response = json.loads(res.body)

                if 'key' in response and response['key'] == image_upload_short_url[1:]:
                    upload_result_flag = True

            except httpclient.HTTPError as e:
                # HTTPError is raised for non-200 responses; the response
                # can be found in e.response.
                logging.warning("Error: " + str(e))
                logging.warning('image not found from upyun: ' + image_upload_short_url)
                upload_result_flag = False

            except upyun.UpYunServiceException as e:
                logging.warning("Error: " + str(e))
                upload_result_flag = False

            except Exception as e:
                logging.warning("Error: " + str(e))
                upload_result_flag = False

        if not upload_result_flag:
            image_upload_short_url = None

        else:
            result = yield self.get_images_from_upyun_async(image_paths=image_upload_short_url)

            if not result:
                image_upload_short_url = None

        raise gen.Return(image_upload_short_url)

    @gen.coroutine
    def get_images_from_upyun_async(self, image_paths):
        image_path_list = []
        if image_paths:
            image_path_list = image_paths.split(',')

        http_client = AsyncHTTPClient(max_clients=125)
        try:
            if len(image_path_list) > 0 and image_path_list[0].startswith('http://'):
                responses = yield [http_client.fetch(image_path + '!exif', raise_error=False, allow_ipv6=False) for
                                   image_path in image_path_list]
            else:
                responses = yield [http_client.fetch("http://7xld8c.com0.z0.glb.qiniucdn.com" + image_path + '!exif',
                                                     raise_error=False, allow_ipv6=False) for image_path in
                                   image_path_list]
            for x in range(len(responses)):
                response = responses[x]
                if response.code == 200:
                    image_info = json.loads(response.body)

                    image_path = image_path_list[x]
                    image_type = image_info.get('type', None)
                    if not image_type:
                        image_type = image_info.get('format', None)
                    self.add_image(image_path, image_type, image_info['width'], image_info['height'])
                else:
                    self.add_image(image_path, 'None', 0, 0)
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            logging.warning("Error: " + str(e))
            logging.warning('image not found from upyun: ' + image_paths)
        except Exception as e:
            # Other errors are possible, such as IOError.
            logging.warning("Error: " + str(e))

        raise gen.Return(True)

    def add_image(self, image_path, image_type, image_width, image_height, fmt=JSON_DICT_FMT):
        if not image_path or not image_type:
            return None

        image = ImageInfoModel()

        image.image_path = image_path
        image.image_type = image_type
        image.image_width = image_width
        image.image_height = image_height

        # result = self.save(image)

        result = self.save_image_into_pika(image_path=image_path, image=image)

        if not result:
            return None

        if fmt == JSON_DICT_FMT:
            return image.to_dict()

        return image

    def save_image_into_pika(self, image_path, image):
        image_json = image.to_json()
        image_json = utils.zlib_compress(image_json)

        try:
            result = self.redis_pika.set(name=resource.IMAGE_KEY + image_path, value=image_json)
        except Exception as e:
            logging.warning(traceback.format_exc())
            return False

        return result
