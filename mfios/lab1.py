import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import kaiserord , lfilter , firwin , freqz
from scipy import fftpack
r=np.arange (1, 20, 1)
#r=6;
hbc=30
hma=1.6
f1=900
C=3
a1=(1.11*np.log10(f1)-0.7)*hma-(1.56*np.log10(f1)-0.8) #поправочный коэффициент
# Модель Cost−Hata
Lcoh=46.3+33.9*np.log10(f1)-13.82*np.log10(hbc)-a1+(44.9-6.55*np.log10(hbc))*np.log10(r)+C
# Модель Okumura−Hata
Lokh=69.55+26.16*np.log10(f1)-13.83*np.log10(hbc)+(44.9-6.55*np.log10(hbc))*np.log10(r)-a1
plt.plot(r, Lcoh, 'r', r, Lokh, 'g')
plt.title("Потери распространения")
plt.xlabel('Расстояние, км')
plt.ylabel('Потери распространения, дБ')
plt.legend(['Cost-Hata', 'Okumura-Hata'])
plt.savefig('потери_распространения.png', dpi=300, bbox_inches='tight')
Pt=35 # мощность передатчика , дБм
Gt=8
Gr=3
Pr=Pt+Gt+Gr-Lcoh
plt.figure(2)
plt.plot(r, Pr)
plt.title("Принятая мощность")
plt.xlabel('Расстояние, км')
plt.ylabel('Мощность на входе приемника')
plt.show()