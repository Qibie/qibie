import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator,FormatStrFormatter

plt.rcParams['font.sans-serif']=['SimHei']

x1=range(1,21)
y1=[15]*20
x2=range(1,21)
y2=[74.96]*20



xmajorLocator=MultipleLocator(1)
xmajorFormatter=FormatStrFormatter('%2d')
xminorLocator=MultipleLocator(0.5)

ymajorLocator=MultipleLocator(10)
ymajorFormatter=FormatStrFormatter('%3d')
yminorLocator=MultipleLocator(5)

ax=plt.subplot(111)

ax.xaxis.set_major_formatter(xmajorFormatter)
ax.xaxis.set_major_locator(xmajorLocator)

ax.yaxis.set_major_locator(ymajorLocator)
ax.yaxis.set_major_formatter(ymajorFormatter)

ax.xaxis.set_minor_locator(xminorLocator)
ax.yaxis.set_minor_locator(yminorLocator)

ax.xaxis.grid(True,which='major')
ax.yaxis.grid(True,which='major')

plt.ylim(0,100)

plt.plot(x1,y1,marker='o',markersize=6,label=u'实验1')
plt.plot(x2,y2,marker='*',markersize=6,label=u'实验2')




plt.legend()
plt.show()