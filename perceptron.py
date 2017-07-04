import random 
#Clase que contiene un perceptron
class Perceptron:
	#Constructor recibe las entradas, los pesos , el sesgo y el 
	def __init__(self,nombre,entradas,pesos,sesgo):
		self.nombre=nombre
		self.entradas=[sesgo]+entradas
		self.sesgo=sesgo
		self.pesos=pesos
	#Te regresa la representacion en string de una neurona	
	def __str__(self):
	   argumentos=self.entradas[1:]
	   cadena=self.nombre+'('+str(argumentos)+')='+str(self.fAct())
	   return cadena
	#Es el set entrada   
	def set_entrada(self,entradas):
		self.entradas=[self.sesgo]+entradas   
	#Te realiza las operaciones entre las entradas y los pesos de las aristas  
	def salida(self):
		n=0;
		longitud=len(self.entradas)
		for i in range(longitud):
			n+=(self.entradas[i]*self.pesos[i])
		return n
	#Te dice si una neurona es o no activada
	def fAct(self):
		if self.salida()<=0:
			return 0
		else:
			return 1
	   
	   
class entrenamiento:
	combinaciones=[[0,0,0],[1,0,1],[0,0,1],[1,1,1]]

	def __init__(self,perceptron,prueba,repeticiones,alfa,resultado=None):
		self.perceptron=perceptron
		self.prueba=prueba
		self.get_pesos_aleatorios()
		self.resultado=resultado
		self.repeticiones=repeticiones
		self.alfa=alfa

	def get_pesos_aleatorios(self):
		for n in range(len(self.prueba[0])):
			self.perceptron.pesos+=[random.uniform(-0.5,0.5)] 

	
	def __str__(self):
		cadena='CONJUNTO DE ENTRENAMIENTO\n'+str(self.prueba)
		cadena+='\nPESOS\n'+str(self.perceptron.pesos)
		cadena+='\nINDICE DE ERROR\n'+str(self.fError())+'\n'
		for c in self.combinaciones:
			self.perceptron.set_entrada(c)
			cadena+=str(self.perceptron)+'\n'

		return cadena
		
	def fError(self):
		return self.resultado-self.perceptron.fAct()
	
	def actualiza_pesos(self): 	
		variable=self.fError()
		for n in range(len(self.perceptron.pesos)):	
			   self.perceptron.pesos[n]+=(self.alfa*self.perceptron.entradas[n]*variable)

	def entrena(self):
		for n in range(self.repeticiones):
			for p in self.prueba:
				self.perceptron.entradas=[self.perceptron.sesgo]+[p[0]]+[p[1]]+[p[2]]
				self.resultado=p[3]
				self.actualiza_pesos()

if __name__=="__main__":
	
	#conjunto de entrenamiento para el and
	p_and_1=[[0,0,0,0],[1,1,1,1]]
	p_and_2=[[0,0,0,0],[0,0,1,0],[0,1,0,0],[0,1,1,0],[1,0,0,0],[1,0,1,0],[1,1,0,0],[1,1,1,1]]
	p_and_3=[[0,0,1,0],[0,1,0,0],[0,1,1,0],[1,0,0,0],[1,0,1,0],[1,1,0,0],[1,1,1,1]]
	p_and_4=[[0,1,0,0],[0,1,1,0],[1,0,0,0],[1,0,1,0],[1,1,0,0],[1,1,1,1]]
	p_and_5=[[0,1,1,0],[1,0,0,0],[1,0,1,0],[1,1,0,0],[1,1,1,1]]
	
	print("ENTRENAMIENTO\n")
	
	
	n_de_entrenamientos=25
	alfa=0.3

	print("AND\n")
	print("Entrenamiento 1")
	and_=Perceptron("and",[],[],-1) 
	entrenar_and=entrenamiento(and_,p_and_1,n_de_entrenamientos,alfa)				
	entrenar_and.entrena()
	print(entrenar_and)
	
	print("Entrenamiento 2")
	and_=Perceptron("and",[],[],-1) 
	entrenar_and=entrenamiento(and_,p_and_2,n_de_entrenamientos,alfa)				
	entrenar_and.entrena()
	print(entrenar_and)
	
	print("Entrenamiento 3")
	and_=Perceptron("and",[],[],-1) 
	entrenar_and=entrenamiento(and_,p_and_3,n_de_entrenamientos,alfa)				
	entrenar_and.entrena()
	print(entrenar_and)
	 
	print("Entrenamiento 4")
	and_=Perceptron("and",[],[],-1) 
	entrenar_and=entrenamiento(and_,p_and_4,n_de_entrenamientos,alfa)				
	entrenar_and.entrena()
	print(entrenar_and)

	print("Entrenamiento 5")
	and_=Perceptron("and",[],[],-1) 
	entrenar_and=entrenamiento(and_,p_and_5,n_de_entrenamientos,alfa)				
	entrenar_and.entrena()
	print(entrenar_and)
 

	p_or_1 =[[0,0,0,0],[1,1,1,1]]
	p_or_2 =[[0,0,0,0],[0,0,1,1],[0,1,0,1],[0,1,1,1],[1,0,0,1],[1,0,1,1],[1,1,0,1],[1,1,1,1]]
	p_or_3 =[[0,0,1,1],[0,1,0,1],[0,1,1,1],[1,0,0,1],[1,0,1,1],[1,1,0,1],[1,1,1,1]]
	p_or_4 =[[0,1,0,1],[0,1,1,1],[1,0,0,1],[1,0,1,1],[1,1,0,1],[1,1,1,1]]
	p_or_5 =[[0,1,1,1],[1,0,0,1],[1,0,1,1],[1,1,0,1],[1,1,1,1]]
	
	
	print("OR\n")

	print("Entrenamiento 1")
	or_=Perceptron("or",[],[],-1) 
	entrenar_or=entrenamiento(or_,p_or_1,n_de_entrenamientos,alfa)				
	entrenar_or.entrena()
	print(entrenar_or)
	
	print("Entrenamiento 2")
	or_=Perceptron("or",[],[],-1) 
	entrenar_or=entrenamiento(or_,p_or_2,n_de_entrenamientos,alfa)				
	entrenar_or.entrena()
	print(entrenar_or)
	
	print("Entrenamiento 3")
	or_=Perceptron("or",[],[],-1) 
	entrenar_or=entrenamiento(or_,p_or_3,n_de_entrenamientos,alfa)				
	entrenar_or.entrena()
	print(entrenar_or)
	 
	print("Entrenamiento 4")
	or_=Perceptron("or",[],[],-1) 
	entrenar_or=entrenamiento(or_,p_or_4,n_de_entrenamientos,alfa)				
	entrenar_or.entrena()
	print(entrenar_or)

	print("Entrenamiento 5")
	or_=Perceptron("or",[],[],-1) 
	entrenar_or=entrenamiento(or_,p_or_5,n_de_entrenamientos,alfa)				
	entrenar_or.entrena()
	print(entrenar_or)
