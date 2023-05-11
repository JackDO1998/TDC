import matplotlib.pyplot as plt
import numpy as np

x = np.random.normal(0, 1, 10000)
i=112
t1="Eingestellt Zeit = "
t2=" ns"
endung=".pdf"
pfad="histogramme/"
titel=t1+str(i)+t2
saveas=pfad+str(i)+t2+endung
plt.hist(x, bins=50);
plt.xlabel("t  /ns")
plt.ylabel("Anzahl der Ereignisse")
plt.title(titel)
plt.savefig(saveas)