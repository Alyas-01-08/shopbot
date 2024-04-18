from os import path
from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup
import lorem
import django
django.setup()
from shop.models import Product, Brand, Category, Size
from shopWebBot.settings import MEDIA_ROOT


host = 'https://www.lamoda.ru'
host_pref = 'https:'
size1 = ['40', '41', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55']
size2 = ['35', '35.5', '36', '36.5', '37', '37.5', '38', '38.5', '39', '39.5', '40', '40.5', '41', '41.5', '42', '42.5',
         '43', '43.5', '44', '44.5', '45']
size3 = ['20', '22', '24', '24', '24', '26', '26', '28', '28', '30']
size4 = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
gender_dict = {
    'men': 'male',
    'women': 'female',
    'children': 'child'
}


def get_soup(url: str):
    resp = requests.get(url)
    return BeautifulSoup(resp.text, 'html.parser')


def get_name_expansion(file: str):
    f_n = path.basename(file)
    n = path.splitext(f_n)
    return n


def get_img(url: str, folder_name: str, name=None):
    p = requests.get(url)
    if not name:
        name = get_name_expansion(url)[0]
    expansion = get_name_expansion(url)[1]
    file_root = '/' + folder_name + '/' + name + expansion
    file_path = MEDIA_ROOT + file_root
    with open(file_path, "wb") as f:
        f.write(p.content)
    return file_root


def pars(soup: BeautifulSoup, size: list[str]):
    urls = [host + i.get('href') for i in soup.find_all('a', class_="x-product-card__link")]
    gender_item = soup.find('a', class_='d-header-genders_link_active').get('data-genders')
    gender = gender_dict.get(gender_item)
    category = soup.find_all('div', class_='x-breadcrumbs__slide')[-1].find('span').get('title')
    res = []
    for u in urls:
        item = get_soup(u)
        brand = item.find('span', class_='x-premium-product-title__brand-name').get_text(strip=True)
        brand_link = host + item.find('a', class_='x-premium-product-title__link').get('href')
        brand_page = get_soup(brand_link)
        brand_img_style = brand_page.find('div', class_='display-quality__img')
        banner_img = brand_page.find('img', class_='ip-banner__img')
        brand_script = item.find_all('script', type='application/ld+json')[-1].text
        brand_json = json.loads(brand_script, strict=False)
        script_image = brand_json[0].get('image')
        if brand_img_style:
            brand_img = host_pref + brand_img_style.get('style').split("'")[1]
        elif banner_img:
            brand_img = host_pref + banner_img.get('src')
        elif len(script_image) > 5:
            brand_img = host_pref + script_image
        else:
            brand_img = None
        title = item.find('div', class_='x-premium-product-title__model-name').get_text(strip=True)
        price = item.find_all('span', class_='x-premium-product-prices__price')[-1].get('content')
        info = lorem.paragraph()
        images = [host_pref + i.get('src') for i in item.find_all('img', class_='x-premium-product-gallery__image')]
        res.append(
            {
                'brand': brand,
                'title': title,
                'price': int(price),
                'info': info,
                'images': images,
                'gender': gender,
                'brand_img': brand_img,
                'size': size
            }
        )
    return res, category


def main(url: str, size: list[str]):
    soup = get_soup(url=url)
    result = pars(soup=soup, size=size)
    category = Category.objects.get_or_create(title=result[1])[0]

    for p in result[0]:
        brand_logo = get_img(url=p['brand_img'], folder_name='brand_icons', name=p['brand']) if p['brand_img'] \
            else '/brand_icons/default_brand.jpg'
        brand = Brand.objects.get_or_create(title=p['brand'], logo=brand_logo)[0]
        brand.category.add(category)
        if product := Product.objects.get_or_none(
                title=p['title'],
                category=category,
                brand=brand,
                gender=p['gender'],
                price=p['price']
        ):
            product.info = p['info']
        else:
            product = Product.objects.create(
                title=p['title'],
                category=category,
                brand=brand,
                gender=p['gender'],
                price=p['price'],
                info=p['info']
            )
        for s in p['size']:
            product.size.add(Size.objects.get_or_create(value=s)[0])
        product_images = [get_img(url=j, folder_name='products') for j in p['images']]
        for img in product_images:
            product.product_img.create(img=img)
    return result


if __name__ == '__main__':
    url1 = 'https://www.lamoda.ru/c/17/shoes-men/'
    url2 = 'https://www.lamoda.ru/c/15/shoes-women/'
    url3 = 'https://www.lamoda.ru/c/5378/default-malchikam/'
    url4 = 'https://www.lamoda.ru/c/559/accs-muzhskieaksessuary/'
    url5 = 'https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/'
    r = main(url=url5, size=size2)
    pprint(r)
    print(len(r[0]))
