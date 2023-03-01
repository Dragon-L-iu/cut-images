import random
from PIL import Image, ImageOps, ImageFilter, ImageChops
import os
import time
import math


class Model:
    CUT = "CUT"
    RANDOM_CUT = "RANDOM_CUT"
    ROTATE = "ROTATE"
    BLUR = "BLUR"


class CutImage:

    def __init__(self, overlap=0, base_x=0, base_y=0):
        self.__RADIUS = None
        self.__name_callback = None
        self.__IMAGE_ROOT = None  # 图片文件所在的文件夹
        self.__LABEL_ROOT = None  # 图片标签所在的文件夹
        self.__BASE_X = base_x  # 开始裁剪的左边坐标
        self.__BASE_Y = base_y  # 开始裁剪的右边坐标
        self.__CUT_WIDTH = None  # 裁剪的宽度
        self.__CUT_HEIGHT = None  # 裁剪的高度
        self.__OVERLAP = overlap  # 裁剪的重叠长度
        self.__ROTATE = 45  # 裁剪的重叠长度
        self.__save_path = None
        self.__save_label_path = None
        self.__model = None
        self.__callback = None

    def __create_save_path(self, image_name, x, y):
        if self.__save_path is None:
            assert "Not set image save path"
        if self.__name_callback is not None:
            return self.__name_callback(image_name, x, y)
        return os.path.join(self.__save_path,
                            image_name.split('.')[0] + "-" + str(y) + str(x) + "." +
                            image_name.split('.')[1])

    def __create_label_save_path(self, label_name, x, y):
        if self.__save_label_path is None:
            assert "Not set label save path"
        if self.__name_callback is not None:
            return self.__name_callback(label_name, x, y)
        return os.path.join(self.__save_label_path,
                            label_name.split('.')[0] + "-" + str(y) + str(x) + "." +
                            label_name.split('.')[1])

    def __min_cut(self, img: Image.Image, base_x, base_y) -> Image.Image:
        """
        use to cut one piece in one image file
        :param img: the Image.Image object
        :param base_x: began cut x position
        :param base_y: began cut y position
        :return: Image.Image
        """
        return img.crop((base_x, base_y, base_x + self.__CUT_WIDTH, base_y + self.__CUT_HEIGHT))

    def __min_rotate(self, img: Image.Image, base_x, base_y) -> Image.Image:
        """
        use to rotate one piece in one image file
        :param img: the Image.Image object
        :param base_x: began cut x position
        :param base_y: began cut y position
        :return: Image.Image
        """
        imge = img.crop((base_x, base_y, base_x + self.__CUT_WIDTH, base_y + self.__CUT_HEIGHT))
        imge = imge.rotate(self.__ROTATE)
        return imge

    def __min_blur(self, img: Image.Image, base_x, base_y, blur=2) -> Image.Image:
        """
        use to rotate one piece in one image file
        :param img: the Image.Image object
        :param base_x: began cut x position
        :param base_y: began cut y position
        :return: Image.Image
        """
        imge = img.crop((base_x, base_y, base_x + self.__CUT_WIDTH, base_y + self.__CUT_HEIGHT))
        imge = imge.filter(ImageFilter.GaussianBlur(blur))
        return imge

    def __no_contain_tuple(self, position_list, x, y):
        for i, j in position_list:
            if i == x and j == y:
                return False
        return True

    # TODO 实现裁剪图片旋转、模糊、反转

    def __image_roate(self, img: Image.Image):
        return img.rotate(45)

    def __image_mirror(self, img: Image.Image):
        return ImageOps.mirror(img)

    def __image_invert(self, img: Image.Image):
        return ImageChops.invert(img)

    def __image_blur(self, img: Image.Image):
        return img.filter(ImageFilter.GaussianBlur(2))

    def set_image_root(self, image_root: str):
        self.__IMAGE_ROOT = image_root

    def set_label_root(self, label_root: str):
        self.__LABEL_ROOT = label_root

    def set_cut_width(self, cut_width: int):
        self.__CUT_WIDTH = cut_width

    def set_cut_height(self, cut_height: int):
        self.__CUT_HEIGHT = cut_height

    def set_overlap(self, overlap: int):
        self.__OVERLAP = overlap

    def set_rotate_deg(self, rotate: int):
        self.__ROTATE = rotate

    def set_save_path(self, save_path: str):
        self.__save_path = save_path

    def set_label_save_path(self, save_path: str):
        self.__save_label_path = save_path

    def set_callback(self, callback):
        self.__callback = callback

    def set_label_callback(self, callback):
        self.__name_callback = callback

    def set_base_point(self, base_point: tuple):
        self.__BASE_X = base_point[0]
        self.__BASE_Y = base_point[1]

    def set_radius(self, radius: int):
        self.__RADIUS = radius

    def cut(self, image_name):
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

    def random_cut(self, image_name, random_count):
        """
        random choose position to cut in one file
        :param callback:
        :param image_name: cut image name
        :param random_count: random cut piece amount in one file
        :param base_x: began cut image x position
        :param base_y: began cut image y position
        :return: None
        """
        assert self.__callback is not None, "没有定义callback函数来完成标签名称的设置"
        label_name = self.__callback(image_name)
        img = Image.open(self.__IMAGE_ROOT + image_name)
        label_img = Image.open(self.__LABEL_ROOT + label_name)
        y_range = math.floor(img.size[1] / self.__CUT_HEIGHT)
        x_range = math.floor(img.size[0] / self.__CUT_WIDTH)
        position_list = []
        if random_count > x_range * y_range:
            print("随机裁剪的数量大于图片本身所能容纳的个数")
        else:
            while len(position_list) < random_count:
                x = random.randint(0, x_range - 1)
                y = random.randint(0, y_range - 1)
                if self.__no_contain_tuple(position_list, x, y):
                    position_list.append((x, y))
                    new_image = self.__min_cut(img, self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                               self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_label_image = self.__min_cut(label_img, self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                                     self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_image.save(self.__create_save_path(image_name, x, y))
                    new_label_image.save(self.__create_label_save_path(label_name, x, y))
                    new_image.close()
                    new_label_image.close()
            img.close()
            label_img.close()

    def random_rotate(self, image_name, random_count=None):
        """
        random choose position to cut in one file
        :param callback:
        :param image_name: cut image name
        :param random_count: random cut piece amount in one file, default is max piece
        :param base_x: began cut image x position
        :param base_y: began cut image y position
        :return: None
        """
        assert self.__callback is not None, "没有定义callback函数来完成标签名称的设置"
        label_name = self.__callback(image_name)
        img = Image.open(self.__IMAGE_ROOT + image_name)
        label_img = Image.open(self.__LABEL_ROOT + label_name)
        y_range = math.floor(img.size[1] / self.__CUT_HEIGHT)
        x_range = math.floor(img.size[0] / self.__CUT_WIDTH)
        position_list = []
        if random_count is None:
            for y in range(y_range):
                for x in range(x_range):
                    new_image = self.__min_rotate(img, self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                                  self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_image.save(self.__create_save_path(image_name, x, y))
                    new_label_image = self.__min_rotate(label_img,
                                                        self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                                        self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_label_image.save(self.__create_label_save_path(label_name, x, y))
                    new_image.close()
                    new_label_image.close()
        else:
            if random_count > x_range * y_range:
                print("随机裁剪的数量大于图片本身所能容纳的个数")
            while len(position_list) < random_count:
                x = random.randint(0, x_range - 1)
                y = random.randint(0, y_range - 1)
                if self.__no_contain_tuple(position_list, x, y):
                    position_list.append((x, y))
                    new_image = self.__min_rotate(img, self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                                  self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_label_image = self.__min_rotate(label_img,
                                                        self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                                        self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_image.save(self.__create_save_path(image_name, x, y))
                    new_label_image.save(self.__create_label_save_path(label_name, x, y))
                    new_image.close()
                    new_label_image.close()
            img.close()
            label_img.close()

    def random_blur(self, image_name, random_count=None):
        """
        random choose position to cut in one file
        :param callback:
        :param image_name: blur image name
        :param random_count: random cut piece amount in one file, default is max piece
        :param base_x: began cut image x position
        :param base_y: began cut image y position
        :return: None
        """
        assert self.__callback is not None, "没有定义callback函数来完成标签名称的设置"
        label_name = self.__callback(image_name)
        img = Image.open(self.__IMAGE_ROOT + image_name)
        label_img = Image.open(self.__LABEL_ROOT + label_name)
        y_range = math.floor(img.size[1] / self.__CUT_HEIGHT)
        x_range = math.floor(img.size[0] / self.__CUT_WIDTH)
        position_list = []
        if random_count is None:
            for y in range(y_range):
                for x in range(x_range):
                    new_image = self.__min_blur(img, self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                                self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_image.save(self.__create_save_path(image_name, x, y))
                    new_label_image = self.__min_blur(label_img,
                                                      self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                                      self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_label_image.save(self.__create_label_save_path(label_name, x, y))
                    new_image.close()
                    new_label_image.close()
        else:
            if random_count > x_range * y_range:
                print("随机裁剪的数量大于图片本身所能容纳的个数")
            while len(position_list) < random_count:
                x = random.randint(0, x_range - 1)
                y = random.randint(0, y_range - 1)
                if self.__no_contain_tuple(position_list, x, y):
                    position_list.append((x, y))
                    new_image = self.__min_blur(img, self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                                self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_label_image = self.__min_blur(label_img,
                                                      self.__BASE_X + self.__OVERLAP + self.__CUT_WIDTH * x,
                                                      self.__BASE_Y + self.__OVERLAP + self.__CUT_HEIGHT * y)
                    new_image.save(self.__create_save_path(image_name, x, y))
                    new_label_image.save(self.__create_label_save_path(label_name, x, y))
                    new_image.close()
                    new_label_image.close()
            img.close()
            label_img.close()

    def process(self, file, model, **kwargs):
        for k, v in kwargs.items():
            if k == "save_path":
                self.__save_path = v
            if k == "random_count":
                random_count = v
        assert self.__save_path is not None, "没有设置保存地址"
        if os.path.isfile(os.path.join(self.__IMAGE_ROOT, file)):
            if model == Model.CUT:
                self.cut(file)
            if model == Model.RANDOM_CUT:
                assert self.__LABEL_ROOT is not None, "没有设置标签图像的根地址"
                self.random_cut(file, random_count=random_count)
            if model == Model.ROTATE:
                assert self.__LABEL_ROOT is not None, "没有设置标签图像的根地址"
                self.random_rotate(file, random_count=random_count)
            if model == Model.BLUR:
                assert self.__LABEL_ROOT is not None, "没有设置标签图像的根地址"
                self.random_blur(file, random_count=random_count)

    def begin(self, model=Model.CUT, **kwargs):
        """
        begin to cut image
        :param model: choose cut approach. default is cut
        :param save_path: use to setting image saving path. default in one directory
        :return:None
        """
        i = 0
        for j, file in enumerate(os.listdir(self.__IMAGE_ROOT)):
            i += 1
            print("\r裁剪中...[%s%s]%d/%d | %s" % (
                '*' * j, ' ' * (len(os.listdir(self.__IMAGE_ROOT)) - j), j, len(os.listdir(self.__IMAGE_ROOT)), file),
                  end='')
            self.process(file, model, **kwargs)

    def run(self, seq: dict, **kwargs):
        assert len(seq) > 0, "传入的处理队列为空"
        count = sum(list(seq.values()))
        i = 0
        k, v = seq.popitem()
        temp = math.floor(len(os.listdir(self.__IMAGE_ROOT)) * v / count)
        for j, file in enumerate(os.listdir(self.__IMAGE_ROOT)):
            if os.path.isfile(os.path.join(self.__IMAGE_ROOT, file)):
                if i < temp:
                    i += 1
                else:
                    i = 0
                    k, v = seq.popitem()
                    temp = math.floor(len(os.listdir(self.__IMAGE_ROOT)) * v / count)
                self.process(file, k, **kwargs)
