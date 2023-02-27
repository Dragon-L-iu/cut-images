from CutImages import CutImage, Model

# 要裁剪的文件夹
IMAGE_ROOT = "F:\photo\\images\\"
LABEL_ROOT = "F:\photo\\labels\\"
# 裁剪结果把保存的文件目录
SAVE_PATH = "F:\photo\\images\\result"
SAVE_LABEL_PATH = "F:\photo\\labels\\result"
# 裁剪的图像宽度
CUT_WIDTH = 200
# 裁剪的图像高度
CUT_HEIGHT = 300


def callback(filename: str):
    name = filename.split(".")
    return name[0] + "_label." + name[1]


# 创建一个CutImage对象
cutimage = CutImage()
cutimage.set_image_root(IMAGE_ROOT)
cutimage.set_cut_width(CUT_WIDTH)
cutimage.set_cut_height(CUT_HEIGHT)
cutimage.set_save_path(SAVE_PATH)
cutimage.set_label_save_path(SAVE_LABEL_PATH)
cutimage.set_label_root(LABEL_ROOT)

cutimage.set_callback(callback)
# 调用begin model参数用来控制裁剪方式
# cutimage.begin(model=Model.CUT, random_count=5)
cutimage.begin(model=Model.RANDOM_CUT, random_count=5)
