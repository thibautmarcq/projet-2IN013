# Module pour prendre des photos des balises avec le gopigo

from robot2IN013 import Robot2IN013

r = Robot2IN013()
f = open("results_camera.txt", "a")

cond = True
while (cond):
	cmd = int(input("0- Quitter le programme\n1- Prendre une photo\n"))
	if cmd==0: 
		cond=False
	elif cmd==1:
		f.write(r.get_images()+'\n') #ou get_image? ou start_recording?
	else :
		pass

f.close()  