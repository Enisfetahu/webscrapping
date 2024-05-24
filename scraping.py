import requests
from bs4 import BeautifulSoup
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext


def scrape_news():
    url = entry.get()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            messagebox.showerror("Error", f"Failed to load page {url} with status code {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        

        articles = soup.find_all(['article', 'div', 'section'])

        news_data = []
        for article in articles:
            title = None
            if article.find('h1'):
                title = article.find('h1').get_text(strip=True)
            elif article.find('h2'):
                title = article.find('h2').get_text(strip=True)
            elif article.find('h3'):
                title = article.find('h3').get_text(strip=True)

            link = article.find('a')['href'] if article.find('a') else ''
            summary = article.find('p').get_text(strip=True) if article.find('p') else ''

            if title:
                news_item = {
                    'title': title,
                    'link': link,
                    'summary': summary
                }
                news_data.append(news_item)
        
        result_text.delete(1.0, tk.END)
        if news_data:
            for item in news_data:
                result_text.insert(tk.END, f"Title: {item['title']}\n")
                result_text.insert(tk.END, f"Link: {item['link']}\n")
                result_text.insert(tk.END, f"Summary: {item['summary']}\n\n")
        else:
            result_text.insert(tk.END, "No articles found.")
        
        with open('news_data.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Scrapper Project Bc10")

frame = tk.Frame(root)
frame.pack(pady=10)

label = tk.Label(frame, text="Enter URL:")
label.pack(side=tk.LEFT)

entry = tk.Entry(frame, width=50)
entry.pack(side=tk.LEFT, padx=10)

button = tk.Button(frame, text="Scrape", command=scrape_news)
button.pack(side=tk.LEFT)

result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.pack(pady=10)

root.mainloop()
