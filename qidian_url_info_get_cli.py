import requests
from bs4 import BeautifulSoup

# 用户输入网址
url = input("请输入网址：")

# 发送HTTP请求获取HTML内容
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取信息
    book_name = soup.find('h1', id='bookName').text.strip()
    writer = soup.find('span', class_='writer').text.strip()

    # 获取书籍简介的标签
    intro_tag = soup.find('p', id='book-intro-detail')

    # 替换<br>标签为换行符，并删除其余HTML标签
    book_intro = intro_tag.get_text(separator='\n', strip=True)

    # 打印结果
    print(f'书名: {book_name}')
    print(f'作者: {writer}')
    print(f'书籍简介:\n{book_intro}')
else:
    print(f'请求失败，状态码: {response.status_code}')
