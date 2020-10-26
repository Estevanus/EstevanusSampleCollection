import bge
import var
import math


def getWaveVol(monoFrames):
	totalFrames = len(monoFrames)
	pembuka = monoFrames[0]
	penutub = monoFrames[-1]
	
	quartal = int(totalFrames / 4)
	half = int(totalFrames / 2)
	
	first = monoFrames[quartal]
	tengah = monoFrames[half]
	second = monoFrames[half + quartal]
	
	a = first - pembuka
	b = tengah - second
	
	hasil = (a + b) / 2
	return hasil, [pembuka, first, second, tengah, monoFrames[-1]]
	
	
def spectud(frames, halfb):
	#plus section
	terkumpulplus = []
	temp_terkumpulplus = []
	
	#min section
	terkumpulmin = []
	temp_terkumpulmin = []
	
	for i in frames:
		if i >= 0:
			#plus section
			temp_terkumpulplus.append(i)
			
			#min section
			if len(temp_terkumpulmin) > len(terkumpulmin):
				terkumpulmin = temp_terkumpulmin
			temp_terkumpulmin = []
			
		else:
			#plus section
			if len(temp_terkumpulplus) > len(terkumpulplus):
				terkumpulplus = temp_terkumpulplus
			temp_terkumpulplus = []
			
			#min section
			temp_terkumpulmin.append(i)
			
	
	jn = 0
	for j in terkumpulplus:
		jn += j
	hp = jn / halfb
		
	
	jn = 0
	for j in temp_terkumpulmin:
		jn += j
	hm = jn / halfb
	
	hasil = hp
	if math.fabs(hm) < hp:
		hasil = math.fabs(hm)
		
	return hasil
	
	
def spectudv0(frames, halfb):
	#plus section
	terkumpulplus = []
	temp_terkumpulplus = []
	
	#min section
	terkumpulmin = []
	temp_terkumpulmin = []
	
	
	for i in frames:
		if i >= 0:
			#plus section
			temp_terkumpulplus.append(i)
			
			#min section
			if len(temp_terkumpulmin) > len(terkumpulmin):
				terkumpulmin = temp_terkumpulmin
			temp_terkumpulmin = []
			
		else:
			#plus section
			if len(temp_terkumpulplus) > len(terkumpulplus):
				terkumpulplus = temp_terkumpulplus
			temp_terkumpulplus = []
			
			#min section
			temp_terkumpulmin.append(i)
			
	
	jn = 0
	for j in terkumpulplus:
		jn += j
	hp = jn / halfb
		
	return hp
	

class KX_SpectObject(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		self.hertz = 60
		
	def setup(self):
		self['hz'] = self.hertz
		self.bytesPerFrame = int(var.frameRate / self.hertz)#this might cause some problem but for now let's just use this math
		
	def run(self):
		fp = len(var.frames)
		if fp >= self.bytesPerFrame:
			frames = var.frames[-self.bytesPerFrame:]
			n, info = getWaveVol(frames)
			self['cek'] = str(info)
			self.scaling = [1, n * 5, 1]
			
	def runv1(self):
		fp = len(var.frames)
		if fp >= self.bytesPerFrame:
			frames = var.frames[-self.bytesPerFrame:]
			n = 0
			for i in frames:
				n += i
				
			hasil = n / self.bytesPerFrame
			self.scaling = [1, hasil * 5, 1]
			
	def runv2(self):
		fp = len(var.frames)
		if fp >= self.bytesPerFrame:
			frames = var.frames[-self.bytesPerFrame:]
			halfb = self.bytesPerFrame / 2
			
			hasil = 0
			jp = 0
			terkumpul = []
			for i in frames:
				if i >= 0:
					jp += 1
					terkumpul.append(i)
					if jp >= halfb / 2:
						jn = 0
						for j in terkumpul:
							jn += j
						
						temph = jn / (halfb / 2)
						if temph > hasil:
							hasil = temph
						break
				else:
					jp = 0
					terkumpul = []
					
			self.scaling = [1, hasil * 5, 1]
			
	def runv3(self):
		fp = len(var.frames)
		if fp >= self.bytesPerFrame:
			frames = var.frames[-self.bytesPerFrame:]
			halfb = self.bytesPerFrame / 2
			
			hasil = spectudv0(frames, halfb)
			self['vol'] = hasil
			
			
			self.scaling = [1, hasil * 5, 1]