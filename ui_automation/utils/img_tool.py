"""
包含了一些与图像相关的工具
TODO: developing
目前比较效果不理想
"""
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
# image_similarity_vectors_


def image_similarity(img1, img2):
    """
    """
    m1 = np.array(img1.resize((400, 400)).convert('L'), dtype=np.uint64)
    m2 = np.array(img2.resize((400, 400)).convert('L'), dtype=np.uint64)
    a = m1.flatten()
    b = m2.flatten()
    cosab = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    return cosab

if __name__ == '__main__':

    img1 = Image.open(r"C:\Users\zheng.zhang\Pictures\Saved Pictures\img1.png")
    img2 = Image.open(r"C:\Users\zheng.zhang\Pictures\Saved Pictures\dog.jpg")
    try:
        similarity = image_similarity(img1, img2)
        print(similarity)
    finally:
        img1.close()
        img2.close()