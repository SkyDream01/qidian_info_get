import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox

def scrape_by_novel_name(novel_name):
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
            result = save_to_file(title, author, website, intro)

            return f"小说信息已保存到 {title}.txt"

    # 如果没有匹配的小说标题
    return "未找到匹配的小说信息"

def scrape_by_url(url):
    # 从 URL 获取 HTML 内容
    response = requests.get(url)
    html_content = response.text

    # 创建 BeautifulSoup 对象
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取标题信息
    title_elem = soup.find('h1', id='bookName')

    # 在访问其文本属性之前检查元素是否已找到
    if title_elem:
        # 获取标题文本
        title = title_elem.text.strip()

        # 提取其他信息
        author_elem = soup.find('span', class_='writer')
        intro_elem = soup.find('p', id='book-intro-detail')

        # 在访问其文本属性之前检查元素是否已找到
        if author_elem:
            author = author_elem.text.strip()
        else:
            author = "作者不可用"

        if intro_elem:
            intro = intro_elem.get_text(separator='\n', strip=True)
        else:
            intro = "简介不可用"

        # 将信息写入表格并保存为文件
        result = save_to_file(title, author, url, intro)

        return f"小说信息已保存到 {title}.txt"

    # 如果没有找到标题
    return "未找到小说信息"

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

    return f"小说信息已保存到 {title}.txt"

def on_search_by_novel_name_click():
    novel_name = entry.get()
    result = scrape_by_novel_name(novel_name)
    messagebox.showinfo("结果", result)

def on_search_by_url_click():
    url = entry.get()
    result = scrape_by_url(url)
    messagebox.showinfo("结果", result)

# 创建主窗口
window = tk.Tk()
window.title("小说信息抓取")

# 创建控件
label = Label(window, text="输入要搜索的小说名称或网址:")
entry = Entry(window)
search_by_novel_name_button = Button(window, text="按小说名称搜索", command=on_search_by_novel_name_click)
search_by_url_button = Button(window, text="按网址搜索", command=on_search_by_url_click)

# 布局控件
label.grid(row=0, column=0, padx=10, pady=10)
entry.grid(row=0, column=1, padx=10, pady=10)
search_by_novel_name_button.grid(row=1, column=0, pady=10)
search_by_url_button.grid(row=1, column=1, pady=10)

# 启动主循环
window.mainloop()
