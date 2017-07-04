"""
Autor=Antonio Martinez Cruz
Practica 5 
"""
class Variable:
	def __init__(self,nombre,valoresPosibles):
		self.nombre=nombre
		self.valoresPosibles=valoresPosibles
	def __str__(self):
		return str(self.nombre)+" en "+str(self.valoresPosibles)		

#Debo de regresa la lista de todas las combinaciones fde valores que pueden tomar las variables
class tabla_de_valores:
	def __init__(self,listaDeVariables):
		self.matriz=[]
		self.listaDeVariables=listaDeVariables
		for i in range(len(listaDeVariables)):
			if i==0 :
				self.add_fst()
			else:
				self.add(i)
	def add_fst(self):
		for valor in self.listaDeVariables[0].valoresPosibles:
			self.matriz.append([valor])	
	def add(self,indice):
		temp=[]
		for j in range (len (self.matriz)):
			for i in range (len (self.listaDeVariables[indice].valoresPosibles)):
				temp.append(self.matriz[j]+[self.listaDeVariables[indice].valoresPosibles[i]])
		self.matriz=temp
	def __str__(self):
		s=""
		for i in range(len(self.matriz)):
				s+=str(self.matriz[i])+"\n"	
		return s
class Factor:
	def __init__(self,alcance,valores,factor=None):
		self.alcance=alcance
		self.tabla_de_valores=tabla_de_valores(alcance)
		self.valores=valores
		self.get_nombres()
		self.factor=factor
		if self.get_num_valores()!=len(valores):
			raise ValueError('el numero de valores\ndeberia de ser '+str(self.get_num_valores())+' y es '+str(len(valores)))
	def get_nombres(self):
		self.nombres=[]
		for i in self.alcance:
			self.nombres+=[i.nombre]	
	def get_num_valores(self):
		n=1
		for variable in self.alcance:
			n*=len(variable.valoresPosibles)
		return n				
	def __str__(self):
		s=" "
		for i in self.alcance:
			s+=str(i.nombre)+"  "

		if self.factor!=None:
			s+="P("+str(self.factor)+")"	
		s+="\n"	
		for i in range(len(self.tabla_de_valores.matriz)):	
				s+=str(self.tabla_de_valores.matriz[i])+" "+str(self.valores[i])+"\n"	
		return s		
	def metodo_auxiliar(self,diccionario):
		return 1
	def get_indice(self,dupla):
		if dupla[0] in self.nombres:
			i=0
			for variable in self.alcance:
				if variable.nombre!=dupla[0]:
					i=i+1
				else:
					break
			j=0		
			for valor in self.alcance[i].valoresPosibles:
				if valor!=dupla[1]:
					j=j+1 
				else:
					break	
			return (i+1,j)		
		return(-1,-1)

	def get_valores(self,lista):
		l=[]
		for t in lista:
			n=1
			for q in range(t[0],len(self.alcance)):
				n=n*len(self.alcance[q].valoresPosibles)
			l.append(n*t[1])
		return l	
	def polinomio_direcc(self,diccionario):
		list=[]
		for i in diccionario:
			temp=self.get_indice([i,diccionario[i]])
			if temp!=(-1,-1):
				list.append(temp)
		list2=self.get_valores(list)
		n=0
		for i in range(len(list2)):
			n+=list2[i]
		valor=0
		for i in diccionario:
			if i not in self.nombres:
				valor=diccionario[i]
		if valor==self.valores[n]:
			return n
		else:
			return -1	

	def aux(self,diccionario):
		list=[]
		for i in diccionario:
			temp=self.get_indice([i,diccionario[i]])
			if temp!=(-1,-1):
				list.append(temp)
		list2=self.get_valores(list)
		n=0
		for i in range(len(list2)):
			n+=list2[i]
		return self.valores[n]
	def get_variable(self,diccionario):
		nombre =None
		for a in diccionario:
			nombre=a
		for variable in self.alcance:
			if variable.nombre==nombre:
				return variable		
def length(alcance):
	n=1
	for variable in alcance:
		n=n*len(variable.valoresPosibles)
	return n
"""
La operacion de multiplicacion es un poco sencilla. Si los conjuntos de variables de
los factores a multiplicar no tienen elementos en comun, se multiplica cada entrada del
factor A por cada entrada del Factor B
"""	
def multiplicacion(factor1,factor2):
	alcance=list(set().union(factor1.alcance,factor2.alcance))
	resultado=Factor(alcance,[0]*length(alcance))
	e=0
	for n in resultado.tabla_de_valores.matriz:
		d1={}
		d2={}
		for i in range(0,len(n)):
			if resultado.alcance[i] in factor1.alcance:
				d1[resultado.alcance[i].nombre]=n[i]
			if resultado.alcance[i] in factor2.alcance:
				d2[resultado.alcance[i].nombre]=n[i]
		resultado.valores[e]=factor1.aux(d1)*factor2.aux(d2)
		e=e+1
	return resultado
"""
La operacion de reduccion consiste en tomar un valor de alguna variable del factor y
solo tomar los renglones que cumplen con el valor dado de la variable. Por ejemplo: Se
tiene el factor AB,
"""
def reduccion(factor1,diccionario):
	if len(diccionario)==1:
		variable=factor1.get_variable(diccionario)
		temp=list(factor1.alcance)
		temp.remove(variable)
		resultado=Factor(temp,[0]*(len(factor1.valores)/len(variable.valoresPosibles)))
		e=0
		for lista in factor1.tabla_de_valores.matriz:
			d1={}
			for i in range(0,len(lista)):
				d1[factor1.alcance[i].nombre]=lista[i]
			if d1[variable.nombre]==diccionario[variable.nombre]:
				resultado.valores[e]=factor1.aux(d1)
				e=e+1	
		return resultado

"""
Para normalizar un factor, basta con sumar todos los valores asociados a las asigna-
ciones y dividir cada uno entre esta suma.
"""
def normalizacion(factor1):
	total=0
	for n in factor1.valores:
		total+=n
	resultado=Factor(list(factor1.alcance),list(factor1.valores))
	for i in range(len(resultado.valores)):
		resultado.valores[i]=resultado.valores[i]/total
	return resultado			
"""
La operacion de marginalizacion consiste en tomar la variable a marginalizar, sumar
los valores en los renglones en que cambia su valor pero el de las demas variables no,
y asignar esta suma al renglon correspondiente de las variables restantes.
"""
def marginalizacion(factor1,variable):
	var=factor1.get_variable({variable:0})
	resultado=Factor([var],[0]*len(var.valoresPosibles))
	e=factor1.nombres.index(variable)
	for lista in factor1.tabla_de_valores.matriz:
		d1={}
		for i in range(0,len(lista)):
			d1[factor1.alcance[i].nombre]=lista[i]
		q=0
		for val in var.valoresPosibles:
			if lista[e]==val:
				resultado.valores[q]=resultado.valores[q]+factor1.aux(d1)
			else:
				q=q+1		
	return normalizacion(resultado)

def get_in(cadena,inicio,fin):
	i=cadena.find(inicio)
	f=cadena.find(fin)
	return cadena[i+1:f]	
def init(lines):
	s=get_in(lines,"[","]")
	r=s.split("},{")
	for i in range(len(r)):
		r[i]=rep(r[i],"{","}")
	return r
def rep(char,rep1,rep2):
	char=char.replace(rep1,"")
	char=char.replace(rep2,"")
	return char
def get_q(var,set):
	for i in set:
		if i.nombre==var:
			return i	
def get_alcance(alcance,variables):
	res=[]
	for i in alcance:
		res.append(get_q(i,variables))
	return res		
def imprime_script():
	#Aqui pruebo la clase factor
	print("Prueba de inicializacion")
	A=Factor([Variable("A",[0,1])],[0.3,0.7])
	print(A)
	B=Factor([Variable("B",[0,1])],[0.6,0.4])
	print(B)
	C=Factor([Variable("C",[0,1])],[0.5,0.5])
	print(C)
	#Pruebo la multiplicacion
	print("Prueba de Multiplicacion\n")
	print("Multiplique A por C\n")
	D=multiplicacion(A,C)
	print(D)
	print("Multiplique B por C\n")
	E=multiplicacion(B,C)
	print(E)
	print("Multiplique (A,B) por (B,C)\n")
	F=multiplicacion(E,D)
	print(F)
	print("Prueba de reduccion")
	print("Tabla A,B")
	J=multiplicacion(A,B)
	print(J)
	print("Lo reduje con A=0")
	J=reduccion(J,{"A":0})
	print(J)
	print("Prueba de normalizacion")
	print("Normalice la siguiente tabla")
	I=Factor([Variable("A",[0,1])],[0.3,2.7])
	print(I)
	I=normalizacion(I)
	print(I)
	print("Prueba de Marginalizacion")
	print("Marginalize B de ABC")
	print(F)
	G=marginalizacion(F,"B")
	print(G)
	print("Marginalize A de AC")
	H=marginalizacion(D,"A")
	print(D)
	print(H)	

def recibetexto(file):
	indice=0
	variables=[]
	numeros=[]
	factores=[]
	alcance=[]
	probas=[]
	for lines in file.readlines():
		if indice==0:
			r=init(lines)	
			for i in range(len(r)):
				s1=r[i].split(":")	
				for w in range(len(s1)):
					s1[w]=rep(s1[w],"'"," ")
				variables.append(s1[0])
				e=s1[1].split(",")
				f=[]
				for t in e :
					f.append(int(t))
				numeros.append(f)
			indice=indice+1
		else :
			if indice==1:
				r=init(lines)
				for i in range(len(r)):
					factores.append(r[i])
				for f in factores:
					k=f.split(",")
					b=[]
					for e in range(len(k)):
						k[e]=k[e].replace(" ","")
						for y in k[e].split("|"):
							b.append(y)
					alcance.append(b)		
				indice=indice+1
			else: 
				if indice==2:
					r=init(lines)
					for i in range(len(r)):
						temp=[]
						f=r[i].split(",")
						for f_ in f:
							temp.append(float(f_.replace(" ","")))    
						probas.append(temp)
					indice=indice+1	
	variables_final=[]
	for i in range(len(variables)):				
		variables_final.append(Variable(variables[i],numeros[i]))
	factores_final=[]
	for i in range(len(factores)):
		factores_final.append(Factor(get_alcance(alcance[i],variables_final),probas[i],factores[i]))		
	file.close()
	return (variables_final,factores_final)

cadena=raw_input("Inserta el nombre del archivo a leer\n")
file=open(cadena,"r")
par=recibetexto(file)
print("Variables")
for variable in par[0]:
	print(variable)
print("Factores")
for factor in par[1]:
	print(factor)
h=raw_input("Quieres que imprima el script de prueba?(S/N)\n")
if h=="S":
	imprime_script()
else:
	print("Bye")	