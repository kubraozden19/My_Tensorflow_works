# -*- coding: utf-8 -*-
"""Tensorflow_Bisiklet_Fiyat_Tahmin_Projesi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M11H37mV8e0UjUYFjN9548v8HpXFifrb
"""

import pandas as pd

dataFrame = pd.read_excel("/content/sample_data/bisiklet_fiyatlari.xlsx")

dataFrame

dataFrame.head() # ilk 5 tanesini gösteriri içinde ne olduğunu görmek amaç

"""**Seaborn Kütüphanesi**

Seaborn, Python programcılarının veri görselleştirmesi yapmak için kullanabileceği bir veri görselleştirme kütüphanesidir. Seaborn, matplotlib tabanlıdır ve daha yüksek düzeyde bir arayüz sağlar, bu nedenle veri görselleştirme işlemleri daha hızlı ve basit hale gelir. Seaborn, özellikle istatistiksel grafikler oluşturmak ve veri analizini daha derinlemesine gerçekleştirmek isteyenler için popüler bir tercihtir.
"""

import seaborn as sbn
import matplotlib.pyplot as plt

sbn.pairplot(dataFrame)  # seaborn kütüphanesini kullanarak her birinin birbirine göre dağılımını grafiklere dökülmüş halini görebiliriz

"""# **Veriyi test ve train olarak ikiye ayırmak**


**Scikit-learn veya sklearn**, Python programcılarının kullanabileceği popüler
bir makine öğrenimi kütüphanesidir. Scikit-learn, açık kaynaklıdır ve geniş bir makine öğrenimi ve veri madenciliği araçları koleksiyonu sunar. Veri madenciliği, veri analizi, veri madenciliği ve makine öğrenimi projeleri için kullanılabilir.

Özellikle makine öğreniminde çok kullanılır burada 2 özelliğini kullandıüımız için pek girmedik ama makine öğreniminde çok kullanılan güzel bir kütüphanedir
"""

from sklearn.model_selection import train_test_split

#train_test_split()

dataFrame   # Y : label dediğimiz yani etiket burada fiyat,     X : features, özelliklerimiz yani burada BisikletOzellik1 ve BisikletOzellik2

# Label yani Y'yi bir diziye, features yani özellikleri X'i bir diziye atamamız gerekiyor

# y = wx + b
# y -> label
y = dataFrame["Fiyat"].values   # values diyerek bunu bir numpy dizisine çevirebiliyoruz

# x -> features(özellik)
x = dataFrame[["BisikletOzellik1","BisikletOzellik2"]].values

# x_train, x_test, y_train, y_test herkes bu değişkenleri kullanır ve bu sırayla veridği için bu sırayla yazmanız önemli
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.33, random_state = 15)  # verilerimizi rastgele alacak şekilde 0.33 oranında bölündü
 # test_size default değeri 0.33 dür.
 # random_state : bu parametrede hangi sayıyı verirseniz bu sayıyı giren herkes için random olarak seçilen veriler aynı veriler olur.Çok da önemli bi şey değil

x_train

x_train.shape

x_test.shape

y_train.shape

y_test.shape

#scaling
#Bu işlem,farklı ölçeklerdeki verileri aynı ölçeğe getirerek veya benzer aralıklarda değerlere sahip verileri oluşturarak,
# verilerin işlenmesini ve karşılaştırılmasını kolaylaştırır. Böylece verilerimizle daha kolay ve daha iyi çalışabilmemiz için kullanıyoruz

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()  #MinMaxScaler sınıfından bir instance yani bir obje oluşturduk işlemleri bunun üzerinden gerçekleştireceğiz

scaler.fit(x_train)

x_train = scaler.transform(x_train)  # direk bu şekilde scale edip atayabiliriz
x_test = scaler.transform(x_test)

x_train   # t_train değerlerinin 0-1 arasına ölçeklendiğini görüyoruz.

import tensorflow as tf
from tensorflow.keras.models import Sequential # modeli oluşturuyormak için
from tensorflow.keras.layers import Dense  # model içerisindeki katmanlar için

from keras.src.engine.training import optimizer
from keras.api._v2.keras import activations
model = Sequential()

model.add(Dense(4, activation = "relu"))
model.add(Dense(4, activation = "relu"))
model.add(Dense(4, activation = "relu"))

model.add(Dense(1))

model.compile(optimizer = "rmsprop", loss = "mse")

# Modelimiz eğitelim

model.fit(x_train,y_train,epochs = 250)

model.history.history

loss = model.history.history["loss"] # loss diye bir dictionary veriyor ya onu diziye çevirdik

sbn.lineplot(x = range(len(loss)), y = loss)

trainLoss = model.evaluate(x_train, y_train, verbose = 0)  # değerlendirme

testLoss = model.evaluate(x_test, y_test, verbose = 0)

trainLoss

testLoss

testTahminleri = model.predict(x_test)

testTahminleri

tahminDF = pd.DataFrame(y_test, columns = ["Gerçek Y"])

tahminDF

testTahminleri = pd.Series(testTahminleri.reshape(330,))

testTahminleri

tahminDF = pd.concat([tahminDF, testTahminleri], axis = 1)

tahminDF

tahminDF.columns = ["Gercek Y", "Tahmin Y"]

tahminDF

sbn.scatterplot( x = "Gercek Y", y = "Tahmin Y", data = tahminDF)

from sklearn.metrics import mean_absolute_error, mean_squared_error

mean_absolute_error(tahminDF["Gercek Y"], tahminDF["Tahmin Y"])

mean_squared_error(tahminDF["Gercek Y"], tahminDF["Tahmin Y"])

dataFrame.describe()

yeniBisikletOzellikleri = [[1750,1749]]

yeniBisikletOzellikleri= scaler.transform(yeniBisikletOzellikleri)

model.predict(yeniBisikletOzellikleri)

# modelimizi kaydedip sonra tekrar ondan tahmin alabilmek için modelimiz kaydedelim

from tensorflow.keras.models import load_model

model.save("bisiklet_modeli.h5")

# sonradanCagirilanModel = load_model("bisiklet_modeli_h5")

sonradanCagirilanModel = load_model("/content/bisiklet_modeli.h5")

sonradanCagirilanModel.predict(yeniBisikletOzellikleri)   # kaydettiğimiz modeli çağırıp tekrar bi tahmin yaptırabiliriz

