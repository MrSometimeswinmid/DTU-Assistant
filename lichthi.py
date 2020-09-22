from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
import os
import os.path
from os import path

ROOT = 'http://pdaotao.duytan.edu.vn'

def get_url_sub(sub, id_, page):
    all_td_tag = []
    for i in range(1, page+1):
        print('http://pdaotao.duytan.edu.vn/EXAM_LIST/?page={}&lang=VN'.format(i))
        r = requests.get('http://pdaotao.duytan.edu.vn/EXAM_LIST/?page={}&lang=VN'.format(i))
        soup = BeautifulSoup(r.text, 'lxml')
        list_td_tag = soup.find_all('td', attrs={'style': 'padding-top:10px'})
        all_td_tag = all_td_tag + list_td_tag

    for td_tag in all_td_tag:
        if (((sub+id_) in str(td_tag.a.contents[0])) or 
        ((sub+' '+id_) in str(td_tag.a.contents[0])) or 
        ((sub+'_'+id_) in str(td_tag.a.contents[0]))):
            print('\nComplete!!!')
            print(' '.join(str(td_tag.a.string).split()))
            print(str(td_tag.a['href']).replace('..', ROOT))
            return str(td_tag.a['href']).replace('..', ROOT)

def get_excel_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    list_span_tags = soup.find_all('span',class_='txt_l4')
    excel_url = list_span_tags[1].a['href'].replace('..',ROOT)
    return excel_url

#ham doi dinh dang file
def change_format(name):
    dau_cham = name.find(".")
    tentep = name[:dau_cham] + name[dau_cham:]
    os.rename(tentep, tentep+'.csv')
    print("Tren tap sau khi thay doi la: " + tentep + ".csv")


# a = get_excel_url('http://pdaotao.duytan.edu.vn/EXAM_LIST_Detail/?ID=52289&lang=VN')

def main():
    sub = input('Nhap ten mon: ')
    id_ = input('Nhap id mon: ')
    url = get_url_sub(sub,id_,4)
    if url == None:
        print('Khong tim thay mon nao nhu nay ({} {}) ca :('.format(sub, id_))
        return
    else:
        print('get excel URL!!!')
        excel_url = get_excel_url(url)
        excel_url = excel_url.replace(' ','%20')
        print('Download excel file!!!')
        save_at = '/home/lucius/Desktop/Hoang/Project/demo/'
        address = save_at + excel_url.split('/')[-1].replace('%20',' ')
        urlretrieve(excel_url,address)

        filename = excel_url.split("/")[-1].replace('%20',' ')
        print(filename)

        if path.exists(filename) == True:
            #đổi định dạng file sau khi tải về
            change_format(filename)
        else:
            print("File chua kip tai ve")
        
        print('Done!')


main()

