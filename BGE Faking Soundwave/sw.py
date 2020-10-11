import bge
import wave
import var
import math
import aud

soundFile = var.lok + "test2.wav"

previewSize = 20

waveInt = 255 * 255#16bit wave
halfWave = waveInt / 2

def init(cont):
	own = cont.owner
	
	#toggle menghilang
	own.visible = False
	
	var.w = wave.open(soundFile)
	w = var.w
	var.frameRate = w.getframerate()
	var.totalFrames = w.getnframes()
	var.totalTime = w.getnframes() / w.getframerate()
	
	cont.activate(cont.actuators['s1'])
	device = aud.device()
	factory = aud.Factory(soundFile)
	handle = device.play(factory)
	
	
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