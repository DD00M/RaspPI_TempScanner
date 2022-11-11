from PIL import Image
from numpy import random as rnd

def map(lista1,lista2):
    img = Image.open('romania.png')
    pixels = img.load() # create the pixel map

    prima=0.00307853 
    doua=0.00456335
    colt1=48.28579
    colt2=19.92

   
    for k in range(len(lista1)):
        lista1[k]=colt1-float(lista1[k])
        lista2[k]=-colt2+float(lista2[k])
        
        lista1[k]=int(lista1[k]/prima)
        lista2[k]=int(lista2[k]/doua)

        #print(lista1[k])
        #print(lista2[k])
    var=10
    for k in range(len(lista1)):
     for i in range(22):
        for j in range(22):
            if lista1[k]+i-11<1550 and lista1[k]+i-11>0 and lista2[k]+j-11>0 and lista2[k]+j-11<2200:
                pixels[lista2[k]+j-11,lista1[k]+i-11] = (15, 239-int(var), 247)
                var+=1
                var=var%239

    img.show()
    img.save('map.png')


listax=[]
listay=[]

listax.append(44.1598)

listay.append(28.6348)
map(listax,listay)
