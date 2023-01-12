from CutImages import CutImage

# 要裁剪的文件夹
IMAGE_ROOT = "F:\photo\\"
# 裁剪结果把保存的文件目录
SAVE_PATH = "F:\photo\\result"
# 裁剪的图像宽度
CUT_WIDTH = 200
# 裁剪的图像高度
CUT_HEIGHT = 300

# 创建一个CutImage对象，传入裁剪文件夹、裁剪宽度，裁剪高度
cutimage = CutImage(IMAGE_ROOT, CUT_WIDTH, CUT_HEIGHT)
# 调用begin 传入保存路径开始裁剪,model参数用来控制
cutimage.begin(model="cut", random_count=5, save_path=SAVE_PATH)
