'''

while true:
	img = cv2.captureVideo(0)
	bbox = detect(img)
	crop_img = crop(img, bbox)
	names = recog(crop, database)
	imshow(bbox, names)

'''