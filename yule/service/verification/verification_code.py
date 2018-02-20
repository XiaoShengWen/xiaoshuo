# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


import string
import random

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from tornado import gen
from yule.lib.service import Service
from yule.lib.singleton import singleton
from yule.service.users.session import SessionService

from yule.database.redis_key.redis_single.sms import SMS_CODE
from yule.database.redis_key.redis_single.sms import SMS_TIMES


@singleton
class VerificationCodeService(Service):
    __session_service = None

    def __init__(self):
        super(Service, self).__init__()
        self.__session_service = SessionService()

    @classmethod
    def generate_verification_code(cls, number=6):
        """
        生成指定位数验证码
        :param number: 位数
        :return:
        """
        return ''.join([random.choice(string.digits + string.ascii_letters) for x in range(number)])

    def check_verification_code(self, session_id, code):
        """
        验证图形验证码
        :param session_id:
        :param code:
        :return:
        """
        sms_code = self.__session_service.get_session(session_id, SMS_CODE)

        if sms_code and code.lower() == sms_code.lower():
            return True
        else:
            return False

    def get_verification_code_image(self, session_id):
        code = self.generate_verification_code(4)

        self.__session_service.set_session(session_id, SMS_CODE, code)

        sms_times = self.__session_service.set_incr_session(session_id, SMS_TIMES)

        if sms_times > 100:
            return False
        else:
            return self.generate_verify_image(code)

    # 生成验证码接口
    def generate_verify_image(self,
                              code_str,
                              size=(124, 66),
                              img_type="GIF",
                              mode="RGB",
                              bg_color=(255, 255, 255),
                              fg_color=(0, 0, 255),
                              font_size=18,
                              font_type="./yule/service/verification/DejaVuSans.ttf",
                              draw_lines=True,
                              n_line=(1, 2),
                              draw_points=True,
                              point_chance=2):

        """
        生成验证码图片
        :param size: 图片的大小，格式（宽，高），默认为(124, 66)
        :param code_str: 验证码字符
        """

        width, height = size
        img = Image.new(mode, size, bg_color)
        draw = ImageDraw.Draw(img)

        def create_lines():

            line_num = random.randint(*n_line)

            for i in range(line_num):
                begin = (random.randint(0, size[0]), random.randint(0, size[1]))
                end = (random.randint(0, size[0]), random.randint(0, size[1]))
                draw.line([begin, end], fill=(0, 0, 0))

        def create_points():

            chance = min(100, max(0, int(point_chance)))

            for w in xrange(width):
                for h in xrange(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=(0, 0, 0))

        def create_strs():

            c_chars = code_str
            strs = ' %s ' % ' '.join(c_chars)

            font = ImageFont.truetype(font_type, font_size)
            font_width, font_height = font.getsize(strs)

            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                      strs, font=font, fill=fg_color)

            return ''.join(c_chars)

        if draw_lines:
            create_lines()
        if draw_points:
            create_points()
        strs = create_strs()

        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = img.transform(size, Image.PERSPECTIVE, params)

        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        mstream = StringIO.StringIO()
        img.save(mstream, img_type)

        return mstream, strs
