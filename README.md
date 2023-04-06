# BizCardX-Extracting-Business-Card-Data-with-OCR
# import os
import os
os.environ["KMP_DUPLICATE_LIB_OK"]  =  "TRUE" # True

-------------------------------------
#import libraries
import pandas as pd
import re
import easyocr
import cv2
import sqlite3
import base64
import streamlit as st
---------------------------------------
#create database as sqlite3
