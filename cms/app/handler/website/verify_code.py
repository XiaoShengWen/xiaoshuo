# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from tornado import gen

from cms.lib.website import BaseWebsiteHandler
from cms.lib.website import system_code
from cms.service.verification.verification_code import VerificationCodeService


class VerifyCodeHandler(BaseWebsiteHandler):

    def prepare(self):
        pass

    @gen.coroutine
    def post(self, *args, **kwargs):
        verification_code_service = VerificationCodeService()

        verify_code = self.get_body_argument('verifyCode', None)
        callback = self.get_body_argument('callback', None)

        result = {
            'image': None,
        }

        if verify_code:
            if verification_code_service.check_verification_code(self.session_id, verify_code):
                code = system_code.SUCCESS
            else:
                code = system_code.VERIFY_ERROR
                code_image, code_str = verification_code_service.get_verification_code_image(self.session_id)

                if code_image:
                    result['image'] = 'data:image/gif;base64,%s' %code_image.getvalue().encode('base64')
        else:
            code = system_code.PARAM_ERROR

        if callback:
            self.render_jsonp(callback, result, code)
        else:
            self.render_json(result, code)
        return

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    @gen.coroutine
    def get(self, *args, **kwargs):
        verification_code_service = VerificationCodeService()
        callback = self.get_body_argument('callback', None)

        code = 0
        result = {
            'image': None,
        }

        if code == 0:
            code_image, code_str = verification_code_service.get_verification_code_image(self.session_id)

            if code_image:
                result['image'] = 'data:image/gif;base64,%s' % code_image.getvalue().encode('base64')
                code = system_code.SUCCESS
            else:
                code = system_code.VERIFY_ERROR

        if callback:
            self.render_jsonp(callback, result, code)
        else:
            self.render_json(result, code)
        return

    def options(self, *args, **kwargs):
        self.write('POST,GET')
