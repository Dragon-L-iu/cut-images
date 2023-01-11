from PIL import Image
import os
import time
import math


class CutImage:
    def __init__(self, image_root, cut_width, cut_height, base_x=0, base_y=0):
        self.IMAGE_ROOT = image_root  # 图片文件所在的文件夹
        self.BASE_X = base_x  # 开始裁剪的左边坐标
        self.BASE_Y = base_y  # 开始裁剪的右边坐标
        self.CUT_WIDTH = cut_width  # 裁剪的宽度
        self.CUT_HEIGHT = cut_height  # 裁剪的高度
        self.save_path = self.IMAGE_ROOT

    def cut(self, image_name, base_x=0, base_y=0):
        """
        cut image for one image file
        :param image_name: use to find image by image_name
        :return: None
        """
        img = Image.open(self.IMAGE_ROOT + image_name)
        y_range = math.floor(img.size[1] / self.CUT_HEIGHT)
        x_range = math.floor(img.size[0] / self.CUT_WIDTH)
        for y in range(y_range):
            for x in range(x_range):
                img2 = img.crop(
                    (base_x, base_y, base_x + self.CUT_WIDTH, base_y + self.CUT_HEIGHT))
                img2.save(os.path.join(self.save_path,
                                       image_name.split('.')[0] + "-" + str(y) + str(x) + "." +
                                       image_name.split('.')[1]))
                base_x += self.CUT_WIDTH
                img2.close()
            base_x = 0
            base_y = base_y + self.CUT_HEIGHT
        img.close()

    def begin(self, **kwargs):
        """
        begin to cut image
        :param save_path: use to setting image saving path
        :return:None
        """
        print(kwargs)
        for k, v in kwargs.items():
            if k == "save_path":
                self.save_path = v
        i = 0
        for file in os.listdir(self.IMAGE_ROOT):
            i += 1
            print("\rcutting...[%s%s]%d/%d | %s" % (
                '*' * i, ' ' * (len(os.listdir(self.IMAGE_ROOT)) - i), i, len(os.listdir(self.IMAGE_ROOT)), file),
                  end='')
            time.sleep(0.5)
            if os.path.isfile(os.path.join(self.IMAGE_ROOT, file)):
                self.cut(file, self.BASE_X, self.BASE_Y)
