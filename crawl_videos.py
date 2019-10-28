import requests
import re
import os

#获取m3u8文件内容
def get_m3u8(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.text
    except:
        print("请求失败")
        return ""

#解析提取ts文件视频地址列表
def parse_video_adr(m3u8):
    #00_h00313wvq89.321002.1.ts?index=0&start=0&end=11880&brs=0&bre=1681659&ver=4
    video_list = re.findall('\d{2,}_.+?ver=\d',m3u8)
    return video_list

#下载视频到本地
def download_video(video_list,prefix_url):
    count = 0
    for v in video_list:
        file_name = re.match('\d{2,}_.+?ts',v).group()
        try:
            video = requests.get(prefix_url+v)
            with open(file_name,'wb') as f:
                f.write(video.content)
            #ts格式转换mp4格式
            new_file_name = file_name[:-2]+'mp4'
            print('已下载完{0}个文件，正在下载文件{1}'.format(count,new_file_name))
            os.system('ffmpeg -i {} -c copy {}'.format(file_name, new_file_name))
            #删除ts格式文件
            os.remove(file_name)
            count = count + 1
        except:
            print("视频下载失败")

def main():
    #视频服务器地址
    prefix_url = 'https://apd-fa90e867c05bd24e1549827b3b7b689a.v.smtcdns.com/moviets.tc.qq.com/AspWP4lvA62Dtao_0pyUetObDU1zyHLPEj8Zb5NRmsdY/uwMROfz2r5xhIaQXGdGnC2df64gZXNTMZvhtgq7maR8xuHpV/U7HOIpdWbGsjip7EpPB3FaV5NGofBQrEy4IgAi44IOWtLdsX8OgbgJXrzPr_VJvFi-MgsEd5giAishet6eX9GyHE-fl1c41VOIFvhLBqfvcbOCWLhMSI0vVpSmIalBKCZW7TKlnrtY1dr4vSpHmckOK775yFbyLbnFYlsgbV9JQ/'
    #m3u8文件地址
    m3u8_url = prefix_url + 'g0024q8zkmq.321004.ts.m3u8?ver=4'

    # 爬取存储目录
    crawl_dir = '/Users/moran/Movies/crawlVideos'
    if not os.path.exists(crawl_dir):
        os.mkdir(crawl_dir)
    os.chdir(crawl_dir)

    m3u8 = get_m3u8(m3u8_url)

    video_list = parse_video_adr(m3u8)

    print('一共{0}个视频文件:{1}'.format(len(video_list),video_list))

    download_video(video_list,prefix_url)

main()