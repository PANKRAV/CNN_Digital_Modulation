# 1. Αναβάθμιση βιβλιοθήκης (για να αποφύγουμε το σφάλμα torchao)
!pip install -q --upgrade torchao

# 2. Σύνδεση με το Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 3. Αποσυμπίεση των εικόνων (αν δεν υπάρχει ήδη ο φάκελος)
import os
if not os.path.exists('/content/images'):
    !unzip -q /content/drive/MyDrive/Telecom_Project/images.zip -d /content/
    print("✅ Το Drive συνδέθηκε και οι εικόνες αποσυμπιέστηκαν!")
else:
    print("✅ Οι εικόνες είναι ήδη έτοιμες!")