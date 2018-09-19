import os
from urllib.request import urlretrieve
import requests

os.makedirs('./img', exist_ok=True)

# 此为资源地址 url
IMAGE_URL = 'https://morvanzhou.github.io/static/img/description/learning_step_flowchart.png'


def use_urllib_download():
    '''
    urllib模块中，提供了有下载功能的urlretrieve
    '''
    # 输入下载地址和存放路径，图片就会自动下载
    urlretrieve(IMAGE_URL, './img/image1.png')  


def use_requests_download():
    '''
        使用requests下载(可以下载大文件，比如视频等...)

    ''' 
    # 方法1
    r = requests.get(IMAGE_URL)
    with open('./image2.png', 'wb') as f:
        f.write(r.content)

    # 方法2
    '''
        使用 r.iter_content(chunk_size) 来控制每个 chunk 的大小, 然后在文件中写入这个 chunk 大小的数据.
    '''
    r = requests.get(IMAGE_URL, stream=True)  # stream loading

    with open('./img/image3.png', 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)


if __name__ == '__main__':
    use_urllib_download()



