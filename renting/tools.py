import pytesseract
import requests
from PIL import Image


# 图像识别获取图片上的所有数字
def img_discern(img):
    image = Image.open(img)
    text = pytesseract.image_to_string(image)
    return text


# 保存图片到本地
def get_image(url):
    """
    :param url: 图片链接参数
    :return: 无返回值，直接保存一张图片
    """
    response = requests.get(url)
    with open("pic_name.png", "wb") as fp:
        for data in response.iter_content(128):
            fp.write(data)


if __name__ == '__main__':
    url = "https://ss0.bdstatic.com/9bA1vGfa2gU2pMbfm9GUKT-w/timg?wisealaddin&sec=1572527689&di=41a098a4d3e58aa60ee824484a5e05c7&quality=100&size=f242_182&src=http%3A%2F%2Fvdposter.bdstatic.com%2F795c11d598d01d5563723ab58c18e838.jpeg%3Fbpoh%3D270%26bpow%3D480"
    get_image(url)
