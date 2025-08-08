from bs4 import BeautifulSoup
import requests

# 读取 HTML 文件
with open('challenge.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

print("开始查找所有 <b class='ref'> 元素...")

# 找到所有符合条件的 <b class="ref">
ref_elements = soup.find_all('b', class_='ref')
print(f"找到 {len(ref_elements)} 个 <b class='ref'> 元素")

url_characters = []

for i, b in enumerate(ref_elements):
    value = b.get('value', '')
    if value:
        # 向上查找父元素来验证结构
        div = b.find_parent('div')
        article = b.find_parent('article')
        section = b.find_parent('section')

        # 验证是否符合完整的模式
        valid = True
        if not (section and section.get('data-id', '').startswith('92')):
            valid = False
        if not (article and article.get('data-class', '').endswith('45')):
            valid = False
        if not (div and '78' in div.get('data-tag', '')):
            valid = False

        if valid:
            url_characters.append({
                'index': i,
                'character': value,
                'section_id': section.get('data-id', ''),
                'article_class': article.get('data-class', ''),
                'div_tag': div.get('data-tag', '')
            })
            print(f"有效字符 {len(url_characters)}: '{value}'")

# 按 DOM 顺序排序
sorted_characters = sorted(url_characters, key=lambda x: x['index'])

# 拼接 URL
hidden_url = ''.join([item['character'] for item in sorted_characters])

print(f"\n隐藏URL字符数: {len(hidden_url)}")
print(f"隐藏URL: {hidden_url}")

# 请求隐藏 URL
try:
    response = requests.get(hidden_url)
    response.raise_for_status()
    print("\n请求成功，返回内容:")
    print(response.text)
except Exception as e:
    print("\n请求失败:", e)
