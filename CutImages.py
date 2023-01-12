import random
from PIL import Image, ImageOps, ImageFilter, ImageChops
import os
import time
import math


class CutImage:
    def __init__(self, image_root, cut_width, cut_height, overlap=0, base_x=0, base_y=0):
        self.__IMAGE_ROOT = image_root  # 图片文件所在的文件夹
        self.__BASE_X = base_x  # 开始裁剪的左边坐标
        self.__BASE_Y = base_y  # 开始裁剪的右边坐标
        self.__CUT_WIDTH = cut_width  # 裁剪的宽度
        self.__CUT_HEIGHT = cut_height  # 裁剪的高度
        self.__OVERLAP = overlap  # 裁剪的高度
        self.__save_path = self.__IMAGE_ROOT
        self.__model = None

    def __create_save_path(self, image_name, x, y):
        return os.path.join(self.__save_path,
                            image_name.split('.')[0] + "-" + str(y) + str(x) + "." +
                            image_name.split('.')[1])

    def __min_cut(self, img: Image.Image, base_x, base_y) -> Image.Image:
        """
        use to cut one piece in one image file
        :param img: the Image.Image object
        :param base_x: began cut x position
        :param base_y: began cut y position
        :return: Image.Image
        """
        return img.crop((base_x, base_y, base_x + self.__CUT_WIDTH, base_y + self.__CUT_HEIGHT))

    def __no_contain_tuple(self, position_list, x, y):
        for i, j in position_list:
            if i == x and j == y:
                return False
        return True

    def set_overlap(self, overlap):
        self.__OVERLAP = overlap

    # TODO 实现裁剪图片旋转、模糊、反转

    def __image_roate(self, img: Image.Image):
        return img.rotate(45)

    def __image_mirror(self, img: Image.Image):
        return ImageOps.mirror(img)

    def __image_invert(self, img: Image.Image):
        return ImageChops.invert(img)

    def __image_blur(self, img: Image.Image):
        return img.filter(ImageFilter.GaussianBlur(2))

    def cut(self, image_name, base_x=0, base_y=0):
        """
        cut image for one image file
        :param image_name: use to find image by image_name
        :return: None
        """
        img = Image.open(self.__IMAGE_ROOT + image_name)
        y_range = math.floor(img.size[1] / self.__CUT_HEIGHT)
        x_range = math.floor(img.size[0] / self.__CUT_WIDTH)
        for y in range(y_range):
            for x in range(x_range):
                new_image = self.__min_cut(img, self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                           self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                new_image.save(self.__create_save_path(image_name, x, y))
                new_image.close()
        img.close()

    def random_cut(self, image_name, random_count, base_x=0, base_y=0):
        """
        random choose position to cut in one file
        :param image_name: cut image name
        :param random_count: random cut piece amount in one file
        :param base_x: began cut image x position
        :param base_y: began cut image y position
        :return: None
        """
        img = Image.open(self.__IMAGE_ROOT + image_name)
        y_range = math.floor(img.size[1] / self.__CUT_HEIGHT)
        x_range = math.floor(img.size[0] / self.__CUT_WIDTH)
        position_list = []
        if random_count > x_range * y_range:
            print("random_count bigger than this picture can cut piece amount")
        else:
            for i in range(random_count):
                x = random.randint(0, x_range - 1)
                y = random.randint(0, y_range - 1)
                if self.__no_contain_tuple(position_list, x, y):
                    position_list.append((x, y))
                    new_image = self.__min_cut(img, self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                               self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_image.save(self.__create_save_path(image_name, x, y))
                    new_image.close()
            img.close()

    def begin(self, model="cut", **kwargs):
        """
        begin to cut image
        :param model: choose cut approach. default is cut
        :param save_path: use to setting image saving path. default in one directory
        :return:None
        """
        print(kwargs)
        for k, v in kwargs.items():
            if k == "save_path":
                self.__save_path = v
            if k == "random_count":
                random_count = v

        i = 0
        for file in os.listdir(self.__IMAGE_ROOT):
            i += 1
            print("\rcutting...[%s%s]%d/%d | %s" % (
                '*' * i, ' ' * (len(os.listdir(self.__IMAGE_ROOT)) - i), i, len(os.listdir(self.__IMAGE_ROOT)), file),
                  end='')
            time.sleep(0.5)
            if os.path.isfile(os.path.join(self.__IMAGE_ROOT, file)):
                if model == "cut":
                    self.cut(file, self.__BASE_X, self.__BASE_Y)
                if model == "random_cut":
                    self.random_cut(file, random_count=random_count)
