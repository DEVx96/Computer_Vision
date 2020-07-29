# -*- coding: utf-8 -*-
"""Cables.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NtPHmoYxFm5tXis2qiF72aQNlulkG8nT
"""

# Commented out IPython magic to ensure Python compatibility.
# %reload_ext autoreload
# %autoreload 2
# %matplotlib inline

from fastai import *
from fastai.vision import *

folder = 'Vga'
filename = 'vga.txt'

folder = 'Hdmi'
filename = 'hdmi.txt'

folder = 'Type-c'
filename = 'typec.txt'

classes = ['Vga','Hdmi']

path = Path('data/cables')
dest = path/folder
dest.mkdir(parents=True,exist_ok = True)

download_images(path/filename,dest,max_pics=200)

for c in classes:
  print(c)
  verify_images(path/c,delete=True,max_workers =8)

np.random.seed(42)
data = ImageDataBunch.from_folder(path,train='.',valid_pct = 0.2,ds_tfms = get_transforms(),size=224).normalize(imagenet_stats)

data.show_batch(rows = 3,figsize=(6,4))

data.classes,data.c,len(data.valid_ds),len(data.train_ds)

learn = cnn_learner(data,models.resnet34,metrics= error_rate)

learn.fit_one_cycle(4)

learn.save("stage-1")

interp = ClassificationInterpretation.from_learner(learn)

interp.plot_top_losses(9,figsize=(10,8))

interp.most_confused()

interp.plot_confusion_matrix()

learn.unfreeze()

learn.lr_find()

learn.recorder.plot()

learn.load('stage-1')

learn.unfreeze()

learn.fit_one_cycle(8,max_lr = slice(4e-05,9e-04))

learn.save('stage-2')

interp = ClassificationInterpretation.from_learner(learn)

interp.most_confused()

interp.plot_top_losses(9)

interp.plot_confusion_matrix()

