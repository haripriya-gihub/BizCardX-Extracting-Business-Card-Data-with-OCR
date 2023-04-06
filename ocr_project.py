import pandas as pd
import re
import easyocr
import cv2
import streamlit as st
import sqlite3
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
# Establishing connection to database
conn = sqlite3.connect('ocrdata.db', check_same_thread=False)
cursor = conn.cursor()
# Creating table in sql
table_create_sql = 'CREATE TABLE IF NOT EXISTS ocr_table(ID INTEGER PRIMARY KEY AUTOINCREMENT,Name TEXT,Address TEXT,Contact_number TEXT,Mail_id TEXT,Website_link TEXT,Image BLOB);'
cursor.execute(table_create_sql)

st.title('Bizcardx Data Extraction')
def upload_database(image):
    # Getting data from image using easyocr
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image, paragraph=True, decoder='wordbeamsearch')
    # converting got data to single string
    data = []
    j = 0
    for i in result:
        data.append(result[j][1])
        j += 1
    data
    org_reg = " ".join(data)
    reg = " ".join(data)
    #Separating EMAIL
    email_regex = re.compile(r'''(
	[a-zA-z0-9]+
	@
	[a-zA-z0-9]+
	\.[a-zA-Z]{2,10}
	)''', re.VERBOSE)
    email = ''
    for i in email_regex.findall(reg):
        email += i
        reg = reg.replace(i, '')
    # separating phone number
    phoneNumber_regex = re.compile(r'\+*\d{2,3}-\d{3,10}-\d{3,10}')
    phone_no = ''
    for numbers in phoneNumber_regex.findall(reg):
        phone_no = phone_no + ' ' + numbers
        reg = reg.replace(numbers, '')
    # Separating Address
    address_regex = re.compile(r'\d{2,4}.+\d{6}')
    address = ''
    for addr in address_regex.findall(reg):
        address += addr
        reg = reg.replace(addr, '')
    # Separating website link
    link_regex = re.compile(r'www.?[\w.]+', re.IGNORECASE)
    link = ''
    for lin in link_regex.findall(reg):
        link += lin
        reg = reg.replace(lin, '')
    # separating Designation (only suitable for this dataset)
        name = reg.strip()

    # reading and getting byte values of image
    with open(image, 'rb') as file:
        blobimg = file.read()
    # inserting data into table
    image_insert = 'INSERT INTO ocr_table (Name,Address,Contact_number,Mail_id,Website_link,Image) VALUES (?,?,?,?,?,?);'
    cursor.execute(image_insert, (name,
                   address, phone_no, email, link, blobimg))


def extracted_data(image):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image, paragraph=True, decoder='wordbeamsearch')
    img = cv2.imread(image)
    for detection in result:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        text = detection[1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.rectangle(img, top_left, bottom_right, (204, 0, 34), 5)
        img = cv2.putText(img, text, top_left, font, 0.8,
                          (0, 0, 255), 2, cv2.LINE_AA)

    # plt.figure(figsize=(10, 10))
    # plt.imshow(img)
    # plt.show()
    return img

