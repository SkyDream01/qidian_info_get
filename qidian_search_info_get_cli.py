import requests
from bs4 import BeautifulSoup

def scrape_book_info(novel_name):
    # 构建动态 URL
    url = f"https://www.qidian.com/so/{novel_name}.html"

    # 从 URL 获取 HTML 内容
    response = requests.get(url)
    html_content = response.text

    # 创建 BeautifulSoup 对象
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找所有书籍项
    book_items = soup.find_all('li', class_='res-book-item')

    # 遍历每个书籍项
    for book_item in book_items:
        # 提取标题信息（如果可用）
        title_elem = book_item.find('h3', class_='book-info-title').find('a', title=True)

        # 在访问其文本属性之前检查元素是否已找到
        if title_elem:
            # 获取<a>中的文本
            title = title_elem.text.strip()
        else:
            title = "标题不可用"

        # 如果小说标题与输入的小说名称匹配，保存信息到文件并返回提示
        if novel_name == title:
            # 提取其他信息
            author_elem = book_item.find('p', class_='author').find('a', class_='name')
            intro_elem = book_item.find('p', class_='intro')

            # 在访问其文本属性之前检查元素是否已找到
            if author_elem:
                author = author_elem.text.strip()
            else:
                author = "作者不可用"

            if intro_elem:
                intro = intro_elem.text.strip()
            else:
                intro = "简介不可用"

            # 提取网站信息
            website_elem = book_item.find('h3', class_='book-info-title').find('a', href=True)
            website = f"https:{website_elem['href']}" if website_elem else "网站不可用"

            # 将信息写入表格并保存为文件
            save_to_file(title, author, website, intro)

            return f"小说信息已保存到 {title}.txt"

    # 如果没有匹配的小说标题
    return "未找到匹配的小说信息"

def save_to_file(title, author, website, intro):
    # 文件名为小说标题.txt
    file_name = f"{title}.txt"

    # 打开文件并写入信息
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write("== 基础信息 ==\n")
        file.write(f"{{| class=\"wikitable\"\n|+\n|作者\n|{author}\n|网站\n|[{website} 起点]\n|-\n|题材\n|\n|状态\n|\n|}}\n\n")
        file.write("== 内容简介 ==\n")
        file.write(f"{intro}\n")
        file.write("[[分类:小说]]\n")


# 示例用法
novel_name = input("输入要搜索的小说名称: ")
result = scrape_book_info(novel_name)
print(result)
