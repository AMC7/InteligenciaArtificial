import random
"""
Antonio Martinez Cruz
312229146
"""
#Clase que representa un tablero de ajedrez
class Tablero:
	#Inicializo el tablero de tamano i con numeros aleatorios
	def __init__(self,i,arreglo=None,aptitud=None):
		self.i=i
		self.arreglo=[-1]*i
		for iu in range(self.i):
			self.add(iu,random.randint(0,i-1))	
		self.getaptitud()
		self.pi=0	

	#Imprimo el tablero con las reinas
	def __str__(self):
		a=""
		temp=[]
		for i in range(len(self.arreglo)):
			temp.append((i,self.arreglo[i]))

		
		for i in range(len(self.arreglo)):
			for j in range(len(self.arreglo)):
				if(j,i)in temp:
				   a+="Q|"
				else:   
				   a+="-|"
			a+="\n"	      
		return a+"\n"+str(self.arreglo)+"\nmax_aptitud=0 \naptitud_actual:"+str(self.aptitud)
	#metodo que te dice si un tablero es igual a otro
	def __eq__(self,other):
		return self.arreglo==other.arreglo	
	#metodob que te compara 2 tableros 
	def __cmp__(self,other):
		if 	self.aptitud==other.aptitud:
			return 0
		if 	self.aptitud<other.aptitud:
			return -1		
		if 	self.aptitud>other.aptitud:
			return 1
		return 0	
	#inserta en la posicion p el objeto o	
	def add(self,p,o):
		if p<self.i:
			self.arreglo[p]=o
	#Checa si hay alguna reina que se choque con otra en horizontal
	def checkHorizontal(self):
		arreglo=sorted(self.arreglo)
		error=0;
		for a in range(self.i-1):
			if arreglo[a]==arreglo[a+1]:
				error=error-1
		return error	

	def checkDiagonalAux(self,tupla):
		t=0;
		for a in range(self.i):
			if tupla[0]!=a:
				if abs(a-tupla[0])==abs(self.arreglo[a]-tupla[1]):
					t=t-1
		return t
	#Checa si hay una reina que choque con otra en diagonal
	def checkDiagonal(self):
		r=0;
		for a in range(self.i):
			r=r+self.checkDiagonalAux((a,self.arreglo[a]))
		return r/2
	#Te dice la aptotud de un tablero
	def getaptitud(self):
		self.aptitud=self.checkHorizontal()+self.checkDiagonal()
	#muta con una baja probabilidad un tablero
	def mutacion(self):
		for q in range(self.i):
			r=random.uniform(0,1)
			if r<0.2:
				self.arreglo[q]=random.randint(0,self.i-1)
		self.getaptitud();		
#combina 2 tableros 
def combina(tablero1,tablero2):
	r=random.randint(0,tablero1.i-1)
	tablero=Tablero(tablero1.i)
	tablero.arreglo=tablero1.arreglo[0:r]+tablero2.arreglo[r:tablero1.i]
	tablero.getaptitud()
	return tablero
#Clase que representa una poblacion
class Poblacion:
	def __init__(self,len,i,generaciones=None,lista=None):
		self.len=len
		self.lista=[]	
		self.generaciones=generaciones
		self.i=i
	#Metodo que llena la poblacion de tableros aleatorios
	def llena(self):
		for w in range(self.len):
			self.lista.append(Tablero(self.i))
	#inserta 5 ejemplares optimos
	def temp(self,other):
		a=max(self.lista)
		for i in range(4):
			other.add(a)
	#Te imprime el tablero		
	def __str__(self):
		s="";
		for n in range(len(self.lista)):
			s+=(str(n)+":\n"+str(self.lista[n])+"\n")	
		return s
	#Obtengo a suma de aptitudes
	def getsumaaptitudes(self):
		suma=0;
		for i in range(self.len):
			suma=suma+self.lista[i].aptitud
		return suma	
	#calcula las probabilidades de que un tablero sea elegido
	def seleccionaux(self):
		suma=self.getsumaaptitudes()
		for i in range(self.len):
			r=self.lista[i].aptitud
			self.lista[i].pi=float(self.lista[i].aptitud)/suma
	#selecciono un tablero aleatorio
	def seleccionRuleta(self):
		i=0
		while True :
			r=random.uniform(0,.1)	
			if(r<self.lista[i%self.len].pi):
				return self.lista[i%self.len]
			else:
				i=i+1
	#Agrego un tablero			
	def add(self,nodo):
		self.lista.append(nodo)				
	#Encuentra el optimo
	def optimo_encontrado(self):
		return max(self.lista).aptitud==0
	#realiza el algoritmo genetico
	def algoritmo_genetico(self):
		i=0
		while ((i<self.generaciones) & (not (self.optimo_encontrado()))):
			nuevaPoblacion=Poblacion(self.len,self.i,self.generaciones)
			self.seleccionaux()
			self.temp(nuevaPoblacion)
			while(len(nuevaPoblacion.lista)<len(self.lista)):
				individuo1=self.seleccionRuleta()
				individuo2=self.seleccionRuleta()
				hijo=combina(individuo1,individuo2)
				hijo.mutacion()
				nuevaPoblacion.add(hijo)
			i=i+1
			if i%50==0:
				print nuevaPoblacion
			self=nuevaPoblacion
		print(str(max(self.lista))+" \niteraciones:"+str(i)+"\n")	
p=Poblacion(50,8,250)
p.llena()
p.seleccionaux()
p.algoritmo_genetico()