# BizCardX-Extracting-Business-Card-Data-with-OCR
1.import requierd libraries 


import pandas as pd

import re

import easyocr

import cv2

import sqlite3

import base64

import streamlit as st


2.import os

os.environ["KMP_DUPLICATE_LIB_OK"]  =  "TRUE"



3.create sqlite database connection
