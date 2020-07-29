# -*- coding: utf-8 -*-
"""tennis-badminton.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o3TCXd6KeGHqBpx9XMZKAPyPSz7NZrhV
"""

# Commented out IPython magic to ensure Python compatibility.
# %reload_ext autoreload
# %autoreload 2
# %matplotlib inline

from fastai import *
from fastai.vision import *

folder = 'tennis'
filename = 'tennis.txt'

folder = 'badminton'
filename = 'badminton.txt'

path = Path('data/sport')
dest = path/folder
dest.mkdir(parents = True,exist_ok = True)

classes = ['tennis','badminton']

download_images(path/filename,dest,max_pics = 200)

for c in classes:
  print(c)
  verify_images(path/c,delete=True,max_workers=8)

data = ImageDataBunch.from_folder(path,train='.',valid_pct=0.2,num_workers = 4,size=224,ds_tfms = get_transforms())

print(data.classes),print(data.c)

len(data.valid_ds)

len(data.train_ds)

data.show_batch(rows=3,figsize=(10,8))

learn = cnn_learner(data,models.resnet34,metrics= error_rate)

learn.fit_one_cycle(4)

interp = ClassificationInterpretation.from_learner(learn)

interp.plot_top_losses(9
                       )

interp.most_confused()

interp.plot_confusion_matrix()

learn.save("stage-1")

learn.unfreeze()

learn.lr_find()

learn.recorder.plot()

learn.load('stage-1')

learn.unfreeze()

learn.fit_one_cycle(4,max_lr=slice(1e-06,1e-04))

interp = ClassificationInterpretation.from_learner(learn)

interp.plot_top_losses(9,figsize=(15,11))

interp.plot_confusion_matrix()

learn.export()

img = open_image(path/'badminton'/'00000024.jpg')
img

learn = load_learner(path)

preds,idxs,outputs = learn.predict(img)

preds

