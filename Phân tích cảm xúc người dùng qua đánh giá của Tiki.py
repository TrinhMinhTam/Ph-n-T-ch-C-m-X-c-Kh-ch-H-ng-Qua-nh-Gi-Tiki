import tkinter as tk
from tkinter import messagebox
import re
import requests
import csv
import os
import pandas as pd
import py_vncorenlp
import json
import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
import matplotlib.pyplot as plt

# Function to preprocess comments
def preprocess_comment(comment):
    rep = {"k": "không", "ko": "không", "kh": "không", "đc": "được",
           "dc": "được", "a": "anh", "e": "em", "v": "vậy",
           "vs": "với", "m": "mình", "!":""} # define desired replacements here
    rep_ = dict((r"\b{}\b".format(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep_.keys()), flags=re.I)
    comment = pattern.sub(lambda m: rep[re.escape(m.group(0)).lower()], comment)
    pattern = r"[?\"'.,!]"
    comment = re.sub(pattern, '', comment)
    return comment

# Function to analyze sentiment
def analyze_sentiment(url):
    # Extract product ID and seller ID from URL
    match = re.search(r'p(\d+).html.*?spid=(\d+)', url)
    if match:
        product_id = match.group(1)
        seller_id = match.group(2)
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy product_id trong URL.")
        return

    # Initialize list to store comments
    list_comment = []

    # Fetch reviews from Tiki API
    url = f'https://tiki.vn/api/v2/reviews?include=comments&product_id={product_id}'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    json_data = result.json()

    # Get total number of pages and reviews
    last_page = json_data['paging']['last_page']
    total_reviews = json_data['paging']['total']

    # Loop through pages to fetch comments
    for i in range(1, last_page+1):
        url = f'https://tiki.vn/api/v2/reviews?include=comments&product_id={product_id}&page={i}'
        result = requests.get(url, headers=headers)
        json_text = result.text
        list_content = json.loads(json_text)['data']
        for content in list_content:
            comment = content['content'].lower()
            rating = content['rating']
            label = 'nothing'
            if comment:
                if rating > 3:
                    label = 'POS'
                elif rating < 3:
                    label = 'NEG'
                else:
                    label = "NEU"
                comment = re.sub(r'[^\w]', ' ', comment)
                comment = re.sub(' +', ' ', comment)
                comment = preprocess_comment(comment)
                row = [comment, label, rating]
                list_comment.append(row)

    # Create folder if it doesn't exist
    output_folder = '/content/input/'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Write comments to CSV file
    with open(output_folder + 'comment.csv', 'w', newline='', encoding='utf-8') as comment_csv:
        writer = csv.writer(comment_csv)
        header = ['comment', 'label', 'rate']
        writer.writerow(header)
        for comment in list_comment:
            writer.writerow(comment)

    # Read comments from CSV
    dataset = pd.read_csv('/content/input/comment.csv')

    # Load VnCoreNLP components
    save_dir = '/content/output'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    py_vncorenlp.download_model(save_dir=save_dir)
    rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=save_dir)

    # Segment Vietnamese text
    dataset_segment = [rdrsegmenter.word_segment(text) for text in dataset['comment']]

    # Load sentiment analysis model
    model = RobertaForSequenceClassification.from_pretrained("wonrax/phobert-base-vietnamese-sentiment")
    tokenizer = AutoTokenizer.from_pretrained("wonrax/phobert-base-vietnamese-sentiment", use_fast=False)

    # Initialize variables to store sentiment scores
    pos = 0
    neu = 0
    neg = 0
    count = 0

    # Analyze sentiment for each comment
    for text in dataset_segment:
        count += 1
        input_ids = torch.tensor([tokenizer.encode(' '.join(text))])
        with torch.no_grad():
            out = model(input_ids)
            result = out.logits.softmax(dim=-1).tolist()
            neg += result[0][0]
            pos += result[0][1]
            neu += result[0][2]

    # Calculate average sentiment scores
    pos_avg = pos / count
    neu_avg = neu / count
    neg_avg = neg / count

    # Plot sentiment distribution
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [pos_avg, neu_avg, neg_avg]
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Sentiment')
    plt.axis('equal')
    plt.show()

    # Display total number of reviews and sentiment scores
    messagebox.showinfo("Kết Quả", f"Tổng số bình luận: {total_reviews}\nBình luận tích cực: {pos_avg*100}%\nBình luận trung lập: {neu_avg*100}%\nBình luận tiêu cực: {neg_avg*100}%")

# Define function to handle button click event
def on_analyze_button_clicked():
    url = url_entry.get()
    analyze_sentiment(url)

# Create main window
root = tk.Tk()
root.title("Phân Tích Cảm Xúc Bình Luận Tiki.vn")

# Create label and entry for URL
url_label = tk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# Create button to trigger sentiment analysis
analyze_button = tk.Button(root, text="Phân tích", command=on_analyze_button_clicked)
analyze_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

root.mainloop()
