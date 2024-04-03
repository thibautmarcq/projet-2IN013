# Module pour prendre des photos des balises avec le gopigo

from robot2IN013 import Robot2IN013
from time import sleep

r = Robot2IN013()
f = open("results_camera.txt", "a")

cond = True
while (cond):
	cmd = input("0- Quitter le programme\n1- Prendre une photo\n")
	if cmd=="0": 
		cond=False
	elif cmd=="1":
		r._start_recording()
		sleep(1/25)
		img = r.get_images()
		f.write(str(img)) #ou get_image? ou start_recording?
		r._stop_recording()

	else :
		pass

f.close()