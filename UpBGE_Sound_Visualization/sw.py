import bge
import wave
import var
import math
import aud

soundFile = var.lok + "test.wav"

previewSize = 14

waveInt = 255 * 255#16bit wave
halfWave = waveInt / 2

def init(cont):
	own = cont.owner
	
	#toggle menghilang
	own.visible = True
	
	var.w = wave.open(soundFile)
	w = var.w
	var.frameRate = w.getframerate()
	var.totalFrames = w.getnframes()
	var.totalTime = w.getnframes() / w.getframerate()
	
	own['totalTime'] = var.totalTime
	
	var.startYPos = own.worldPosition.y
	
	cont.activate(cont.actuators['s1'])
	
	device = aud.Device()
	factory = aud.Sound(soundFile)
	handle = device.play(factory)
	var.isStart = True
	var.handle = handle
	
	
def run(cont):
	own = cont.owner
	waktu = own['waktu']
	
	curFrame = int(waktu / var.totalTime * var.totalFrames)
	
	panjangPita = int(math.fabs(curFrame - var.lastFrame +1))
	#frame = var.w.readframes(735)
	frame = var.w.readframes(panjangPita)
	b = frame[-4:-2]
	own['cek'] = str(panjangPita)
	nilai = int.from_bytes(b, 'little')
	#nilai = b[1] * 255 + b[0]
	
	hn = nilai / (waveInt)
	if hn > 0.5:
		#hn = 1 - hn
		hn = hn -1
	n = hn * previewSize * 2
	
	#apply scaling
	own['skala'] = n
	own.scaling = [1 , n , 1]
	
	#drawing laser
	#bge.render.drawLine([0, n, 0], [0, var.lastN, 0], [0, 1, 0])
	
	var.lastFrame = curFrame
	var.lastN = n
	
	#take snapshot
	#if waktu < var.totalTime:
	#	bge.render.makeScreenshot("sw")
	
	
def runV2(cont):
	own = cont.owner
	waktu = own['waktu']
	
	curFrame = int(waktu / var.totalTime * var.totalFrames)
	
	panjangPita = int(math.fabs(curFrame - var.lastFrame +1))
	#frame = var.w.readframes(735)
	frame = var.w.readframes(panjangPita)
	b = frame[-4:-2]
	own['cek'] = str(panjangPita)
	nilai = int.from_bytes(b, 'little')
	#nilai = b[1] * 255 + b[0]
	
	hn = nilai / (waveInt)
	if hn > 0.5:
		#hn = 1 - hn
		hn = hn -1
	n = hn * previewSize
	
	own['n'] = n
	if own.worldPosition.x > -13:
		own.worldPosition = [own.worldPosition.x - 0.1 , n , 0]
	else:
		own.worldPosition = [-13 , n , 0]
	
	#drawing laser
	#bge.render.drawLine([0, n, 0], [0, var.lastN, 0], [0, 1, 0])
	
	var.lastFrame = curFrame
	var.lastN = n
	
	
def runV3(cont):
	own = cont.owner
	waktu = var.handle.position
	own['waktu'] = waktu
	
	
	if var.isStart:
		curFrame = int(waktu / var.totalTime * var.totalFrames)
		
		panjangPita = int(math.fabs(curFrame - var.lastFrame +1))
		#frame = var.w.readframes(735)
		frame = var.w.readframes(panjangPita)
		
		b = frame[-2:]
		own['framePerTick'] = panjangPita
		hn = 0
		if var.isPlus == 1:
			for i in range(int(len(frame) / 2)):
				ke = (i+1)*2
				curb = frame[ke - 2 :ke]
				nilai = int.from_bytes(b, 'little')
				
				tn = nilai / (waveInt)
				if tn > 0.5:
					#hn = 1 - hn
					tn = tn -1
					var.isPlus = -1
				
				tn = math.fabs(tn)
				
				if tn > hn:
					hn = tn
					
				if tn * 2 > own['biggestValue']:
					own['biggestValue'] = tn * 2
		else:
			for i in range(int(len(frame) / 2)):
				ke = (i+1)*2
				curb = frame[ke - 2 :ke]
				nilai = int.from_bytes(b, 'little')
				
				tn = nilai / (waveInt)
				if tn > 0.5:
					#hn = 1 - hn
					tn = tn -1
				else:
					var.isPlus = 1
				
				
				if tn < hn:
					hn = tn
					
				if math.fabs(tn) * 2 > own['biggestValue']:
					own['biggestValue'] = math.fabs(tn) * 2
			
		
		n = hn * previewSize
		
		own['n'] = n
		batas = -14.8
		if own.worldPosition.x > batas:
			own.worldPosition = [own.worldPosition.x - 0.1 , n + var.startYPos , 0]
		else:
			own.worldPosition = [batas , n + var.startYPos , 0]
		
		keyboard = bge.logic.keyboard
		#if cont.sensors['screenshot'].getKeyStatus == True:
		if keyboard.events[bge.events.TKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED:
			bge.render.makeScreenshot(var.lok + "scr/cool-#")
		
		var.lastFrame = curFrame
	
def pp(cont):
	own = cont.owner
	
	aktif = True
	for i in cont.sensors:
		if i.positive == False:
			aktif = False
			
	if aktif:
		if var.isStart:
			var.handle.pause()
			var.isStart = False
		else:
			var.handle.resume()
			var.isStart = True
		
	
	
	