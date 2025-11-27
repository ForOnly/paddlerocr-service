# @description: 
# @author: licanglong
# @date: 2025/6/25 9:04
# hook-paddleocr.py
from PyInstaller.utils.hooks import collect_all

# 把 handlers 及其所有子包全部打进 hiddenimports
datas, binaries, hiddenimports = collect_all('paddleocr')
