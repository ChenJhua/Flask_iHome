# coding=utf-8
import qiniu


access_key = ""
secret_key = ""
# 存储空间的名称
bucket_name = "ihome-sz08"


def storage_image(data):
    """上传文件至七牛云"""
    # 认证
    q = qiniu.Auth(access_key, secret_key)
    # 指定上传后的文件名
    # key = 'hello'
    # 上传文件的内容
    # data = 'hello qiniu!'
    # 指定上传文件到七牛云中的哪个存储空间
    token = q.upload_token(bucket_name)
    # 上传文件到七牛云
    ret, info = qiniu.put_data(token, None, data)

    # print ret
    # print info
    if info.status_code == 200:
        # 上传成功
        key = ret.get("key")
        return key
    else:
        # 上传失败
        raise Exception("上传文件到七牛云失败")


if __name__ == '__main__':
    filename = raw_input("请输入上传文件的名称：")
    with open(filename, "rb") as f:
        storage_image(f.read())

