#1. Load the image and Waldo template
file2 = 'waldo_onIce.png'
file2Temp = 'waldo_template.png'

img1 = load_img(folder_Path + file2)
temp1 = load_img(folder_Path + file2Temp)

#Convert the two images to grayscale
img = color.rgb2gray(img1)
temp = color.rgb2gray(temp1)

#Display the 2 images
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
ax = axes.ravel()
ax[0].imshow(img1)
ax[1].imshow(temp1)
fig.tight_layout()

def _convolve(a,b):
  tot = np.sum(np.multiply(a,b))
  return tot

def crosscorr(Img, f):
    tempH, tempW = f.shape
    H, W = Img.shape
    G = Img
    for i in range(H-tempH):
      for j in range(W-tempW):
        G[i,j] = _convolve(f, Img[i:i+tempH, j:j+tempW])

    return G

G = crosscorr(img,temp)
plt.figure()
plt.imshow(G, cmap=plt.cm.gray)


#3. Use the helper function 'draw_patch' to place a circular cyan patch on 
# the presumed location of Waldo on the original image. Also, display the 
# image of the correlation map obtained alongside the image. 
# 
result = np.where(G == np.amax(G))
listOfCoordinates = list(zip(result[0],result[1]))
y = listOfCoordinates[0][0]
x = listOfCoordinates[0][1]
print(x,y)
xy=(x,y)
fig, ax = plt.subplots()
ax.imshow(img1)
ax.add_patch(patches.Circle(xy, radius=20, edgecolor='cyan',facecolor='cyan', fill=True))

plt.show()

def _normcrosscorr(Img, f):
  tot = np.sum(np.multiply(Img,f))
  return tot

def normcrosscorr(Img, f):
  ImgMean = np.mean(Img)
  fMean = np.mean(f)
  ImgDen = np.sum((Img-ImgMean)**2)
  fDen = np.sum((f-fMean)**2)
  normImg = (Img-ImgMean)/np.sqrt(ImgDen)
  normf = (f-fMean)/np.sqrt(fDen)
  tempH, tempW = normf.shape
  H, W = normImg.shape
  G = normImg
  for i in range(H-tempH):
    for j in range(W-tempW):
      G[i,j] = _normcrosscorr(normImg[i:i+tempH, j:j+tempW],normf )

  return G

G = normcrosscorr(img,temp)

plt.imshow(G, cmap=plt.cm.gray)
#5. Again, use the helper function 'draw_patch' to place a circular green patch on 
# the presumed location of Waldo on the original image. Also, display the 
# image of the normalized correlation map obtained alongside the image. 
# 
result = np.where(G == np.amax(G))
listOfCoordinates = list(zip(result[0],result[1]))
y = listOfCoordinates[0][0]
x = listOfCoordinates[0][1]
print(x,y)
xy=(x,y)
fig, ax = plt.subplots()
ax.imshow(img1)
ax.add_patch(patches.Circle(xy, radius=20, edgecolor='green',facecolor='green', fill=True))

#6. Write and call an SSD function to find the best match for Waldo
def _Z(I,f):
  ssd = np.sum(I-f)
  return ssd

def SSD(Img, f):
  tempH, tempW = f.shape
  H, W = Img.shape
  G = img
  for i in range(H-tempH):
    for j in range(W-tempW):
      G[i,j] = _Z(Img[i:i+tempH, j:j+tempW],f)
  return G
    
G = SSD(img,temp)
plt.imshow(G,cmap=plt.cm.gray)

#7. Lastly, use the helper function 'draw_patch' to place a circular red patch on 
# the presumed location of Waldo on the original image. Also, display the 
# image of the SSD map obtained alongside the image. 
# 
result = np.where(G == np.amin(G))
listOfCoordinates = list(zip(result[0],result[1]))
y = listOfCoordinates[0][0]
x = listOfCoordinates[0][1]
print(x,y)
xy=(x,y)
fig, ax = plt.subplots()
ax.imshow(img1)
ax.add_patch(patches.Circle(xy, radius=20, edgecolor='red',facecolor='red', fill=True))

plt.show()
