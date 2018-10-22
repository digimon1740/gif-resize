import glob, os
from subprocess import call
from subprocess import check_output, check_call
from shutil import copyfile

if __name__ == "__main__":
    width = 1080
    quality = 90
    ext = '.gif'
    size = "{}x{}".format(width, 505)
    # blob 으로 데이터를 받느다.
    f = open('/Users/digimon/Downloads/gif/original_s3.gif', "rb")
    bytes = f.read()

    # blob 데이터를 임시폴더에 에피소드명_해상도_퀄리티.gif 로 저장한다.

    tmp = './uploads/original_{}_{}.gif'
    nf = open(tmp.format(width, quality, ext), "wb")
    nf.write(bytes)
    # gifsicle 로 저장된 gif 를 리사이징한다.
    print(
        call(["gifsicle", "-O3", "--colors", "256", '--resize', size, '/Users/digimon/Downloads/gif/original_s3.gif', "-o",
              '/Users/digimon/Downloads/gif/original_s3_converted.gif']))
    # 리사이징된 gif 파일을 bytes 로 읽어 들인후 tmp 파일 삭제

    #
    #
