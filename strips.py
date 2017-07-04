# coding=utf-8
# ------ Dominio -----
import itertools
class Dominio:
    """ Clase para definir el dominio, o espacio de estados en el cual se plantearán problemas de planeación. """
    def __init__(self, nombre, tipos, predicados, acciones):
        """
        Inicializa un dominio
        :param nombre:
        :param tipos:
        :param predicados:
        :param acciones:
        """
        self.nombre = nombre
        self.tipos = tipos
        self.predicados = predicados
        self.acciones = acciones

    def __str__(self):
        dic = {'name':          self.nombre,
               'types':         "  \n".join(self.tipos),
               'predicates':    "  \n".join(str(p) for p in self.predicados),
               'actions':       "\n".join(str(a) for a in self.acciones)
               }
        return """(define (domain {name})
          (:requirements :strips :typing)
          (:types
            {types})
          (:predicates
            {predicates})
          )
          {actions})
        """.format(**dic)


class Variable:
    """ Variable tipada. """
    def __init__(self, nombre, tipo, valor=None):
        """
        :param nombre: símbolo nombre de esta variable.  Los nombres de variables inician con ?
        :param tipo: tipo de la variable, debe estar registrado en la descripción del dominio
        :param valor: objeto vinculado a esta variable, si es None la variable está libre
        """
        self. nombre = nombre
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        if self.valor:
            return self.valor.nombre
        return "{} - {}".format(self.nombre, self.tipo)
    def __eq__(self,other):    
       return (self.nombre==other.nombre)and(self.tipo==other.tipo)and (self.valor==other.valor)
    def __hash__(self):
       return hash((self.nombre,self.tipo,self.valor))        

class Predicado:
    """ Representa un hecho. """
    def __init__(self, nombre, variables, negativo = False):
        """
        Predicados para representar hechos.
        :param nombre:
        :param variables: lista de variables tipadas
        :param negativo: indica un predicado del tipo "no P", utilizable para especificar efectos o metas.
        """
        self.nombre = nombre
        self.variables = variables
        self.negativo = negativo

    def __str__(self):
        pred = "({0} {1})".format(self.nombre, " ".join(str(v) for v in self.variables))
        if self.negativo:
            return "(not {0})".format(pred)
        return pred
    def __eq__(self,other):
        return (self.nombre==other.nombre)and(self.variables==other.variables)and(self.negativo==other.negativo)  

class Accion:
    """ Función de transición con su acción correspondiente. """
    def __init__(self, nombre, parametros, precondiciones, efectos, vars=None):
        """
        Inicializa definición de la función de transición para esta acción.
        :param nombre: nombre de la acción
        :param parámetros: lista de variables tipadas
        :param precondiciones: lista de predicados con variables libres
        :param efectos: lista de predicados con variables libres
        :param vars: lista de variables libres que pueden tomar su valor de cualquier objeto del domino simpre que
               sus valores satisfagan las restriciones de las precondiciones.
        """
        self.nombre = nombre
        self.parametros = parametros
        self.precondiciones = precondiciones
        self.efectos = efectos
        self.vars = vars

    def __str__(self):
        dic = {'name':      self.nombre,
               'params':    " ".join(str(p) for p in self.parametros),   # Podrían reunirse 1o los de tipos iguales
               'prec':      " ".join(str(p) for p in self.precondiciones),
               'efec':      " ".join(str(p) for p in self.efectos)
               }
        if self.vars:
            dic['vars'] = "\n    :vars {}".format(" ".join(str(v) for v in self.vars))
        else:
            dic['vars'] = ""
        return """(:action {name}
            :parameters   ({params}) {vars}
            :precondition (and {prec})
            :effect       (and {efec})
        )
        """.format(**dic)


# ------ Problema -----

class Objeto:
    """ Valor concreto para variables en el dominio. """
    def __init__(self, nombre, tipo):
        """
        Crea un objeto existente en el dominio para este problema.
        :param nombre: Símbolo del objeto
        :param tipo: tipo del objeto
        """
        self.nombre = nombre
        self.tipo = tipo

    def __hash__(self):
        return hash((self.nombre,self.tipo))
    def __eq__(self,other): 
        return self.nombre==other.nombre and self.tipo==other.tipo
    def __str__(self):
        return "{} - {}".format(self.nombre, self.tipo)

class Sustitucion_aplicable:
    def __init__(self,hechos,sustitucion):
        self.hechos=hechos
        self.sustitucion=sustitucion
class Nodo:
    def __init__(self,listaDeHijos,padre,visitado=None):
         self.listaDeHijos=listaDeHijos
         self.padre=padre
         self.visitado=visitado

class Grafica: 
      def __init__(self,raiz):
        self.raiz=raiz   
class Problema:
    """ Definicion de un problema en un dominio particular. """
    def __init__(self, nombre, dominio, objetos, predicados, predicados_meta):
        """
        Problema de planeación en una instancia del dominio.
        :param nombre: nombre del problema
        :param dominio: referencia al objeto con la descripción genérica del dominio
        :param objetos: lista de objetos existentes en el dominio, con sus tipos
        :param predicados: lista de predicados con sus variables aterrizadas, indicando qué cosas son verdaderas en el
               estado inicial.  Todo aquello que no esté listado es falso.
        :param predicados_meta: lista de predicados con sus variables aterrizadas, indicando aquellas cosas que deben
               ser verdaderas al final.  Para indicar que algo debe ser falso, el predicado debe ser negativo.
        """
        self.nombre = nombre
        self.dominio = dominio # ref a objeto Dominio
        self.objetos = objetos
        self.estado = predicados
        self.meta = predicados_meta

    def __str__(self):
        dic = {'name':          self.nombre,
               'domain_name':   self.dominio.nombre,
               'objects':       "\n".join(str(o) for o in self.objetos),
               'init':          "\n".join(str(p) for p in self.estado),
               'goal':          "\n".join(str(p) for p in self.meta)}
        return """(define (problem {name}
          (:domain {domain_name})
          (:objects
            {objects})
          (:init
            {init})
          (:goal
            (and {goal}))
        )
        """.format(**dic)

def combinaciones(accion,problema):
     parametros=[] 
     for parametro in accion.parametros+accion.vars:
        a=[]
        for objeto in problema.objetos: 
          if parametro.tipo==objeto.tipo:
               a.append(objeto)
        parametros.append(a)
        
     return list(itertools.product(*parametros))

def mismo_tipo(variable,lista):
    for i in lista:
       if i.tipo==variable.tipo:
         return True
    return False            

if __name__ == '__main__':
    print("Este es el ejemplo del libro");
    """ Aqui estoy declarendo mis predicados"""
    adjacent=Predicado('adjacent',[Variable('?l1','location'),Variable('?l2','location')]);
    attached=Predicado('attached',[Variable('?p','pile'),Variable('?l','location')]);
    belong=Predicado('belong',[Variable('?k','crane'),Variable('?l','location')]);

    at=Predicado('at',[Variable('?r','robot'),Variable('?l','location')]);
    occupied=Predicado('occupied',[Variable('?l','location')]);
    loaded=Predicado('loaded',[Variable('?r','robot'),Variable('?c','container')]);
    unloaded=Predicado('unloaded',[Variable('?r','robot')]);
    holding=Predicado('holding',[Variable('?k','crane'),Variable('?c','container')]);
    empty=Predicado('empty',[Variable('?k','crane')]);

    inp=Predicado('in',[Variable('?c','container'),Variable('?p','pile')]);
    top=Predicado('top',[Variable('?c','container'),Variable('?p','pile')]);
    on=Predicado('on',[Variable('?k1','container'),Variable('?k2','container')]);
    """Agrego el negativo"""
    nadjacent=Predicado('adjacent',[Variable('?l1','location'),Variable('?l2','location')],True);
    nattached=Predicado('attached',[Variable('?p','pile'),Variable('?l','location')],True);
    nbelong=Predicado('belong',[Variable('?k','crane'),Variable('?l','location')],True);

    nat=Predicado('at',[Variable('?r','robot'),Variable('?l','location')],True);
    noccupied=Predicado('occupied',[Variable('?l','location')],True);
    nloaded=Predicado('loaded',[Variable('?r','robot'),Variable('?c','container')],True);
    nunloaded=Predicado('unloaded',[Variable('?r','robot')],True);

    nholding=Predicado('holding',[Variable('?k','crane'),Variable('?c','container')],True);
    nempty=Predicado('empty',[Variable('?k','crane')],True);

    ninp=Predicado('in',[Variable('?c','container'),Variable('?p','pile')],True);
    ntop=Predicado('top',[Variable('?c','container'),Variable('?p','pile')],True);
    non=Predicado('on',[Variable('?k1','container'),Variable('?k2','container'),True]);

    move=Accion('move',
        [Variable('?r','robot'),Variable('?from','location'),Variable('?to','location')],
        [adjacent,at,noccupied],
        [at,noccupied,occupied,nat],
        []);

    load=Accion('load',
        [Variable('?k','crane'),Variable('?c','container'),Variable('?r','robot')],
        [at,belong,holding,unloaded],
        [loaded,nunloaded,empty,nholding],
        [Variable('?l','location')]); 

    unload=Accion('unload',
        [Variable('?k','crane'),Variable('?c','container'),Variable('?r','robot')],
        [belong,at,loaded,empty],
        [unloaded,holding,nloaded,nempty],
        [Variable('?l','location')]);

    take=Accion('take', 
        [Variable('?k',"crane"),Variable('?c','container'),Variable('?p','pile')],
        [belong,attached,empty,inp,top,on],
        [holding,top,ninp,ntop,non,nempty],
        [Variable('?l','location'),Variable('?else','container')]);

    put=Accion('put',
        [Variable('?k','crane'),Variable('?c','container'),Variable('?p','pile')],
        [belong,attached,holding,top],
        [inp,top,on,ntop,nholding,empty],
        [Variable('?c','container'),Variable('?l','location')]);

    

    """Declerando mis acciones"""    

    dominio=Dominio('dock-worker-robot',
                    ['location','pile','crane','robot','container'],
                    [adjacent,attached,belong,at,occupied,loaded,unloaded,empty,inp,top,on],
                    [move,load,unload,take,put]);
    """Definimos los objetos del problema"""
    or1=Objeto('r1','robot')
    ol1=Objeto('l1','location')
    ol2=Objeto('l2','location')
    locaciones=[ol1,ol2]
    ok1=Objeto('k1','crane')
    ok2=Objeto('k2','crane')
    gruas=[ok1,ok2]
    op1=Objeto('p1','pile')
    oq1=Objeto('q1','pile')
    op2=Objeto('p2','pile')
    oq2=Objeto('q2','pile')
    pilas=[op1,oq1,op2,oq2]
    oca=Objeto('ca','container')
    ocb=Objeto('cb','container')
    occ=Objeto('cc','container')
    ocd=Objeto('cd','container')
    oce=Objeto('ce','container')
    ocf=Objeto('cf','container')
    contenedores=[oca,ocb,occ,ocd,oce,ocf]
    opallet=Objeto('pallet','container')

    p1=Predicado('adjacent',[Variable('?l1','location',ol1),Variable('?l2','location',ol2)])
    p2=Predicado('adjacent',[Variable('?l2','location',ol2),Variable('?l1','location',ol1)])

    p3=Predicado('attached',[Variable('?p1','pile',op1),Variable('?l1','location',ol1)])
    p4=Predicado('attached',[Variable('?q1','pile',oq1),Variable('?l1','location',ol1)])
    p5=Predicado('attached',[Variable('?p2','pile',op2),Variable('?l2','location',ol2)])
    p6=Predicado('attached',[Variable('?q2','pile',oq2),Variable('?l2','location',ol2)])
   
    p7=Predicado('belong',[Variable('?k1','crane',ok1),Variable('?l1','location',ol1)])
    p8=Predicado('belong',[Variable('?k2','crane',ok2),Variable('?l2','location',ol2)])
    
    p9 =Predicado('in',[Variable('?ca','container',oca),Variable('?p1','pile',op1)]);
    p10=Predicado('in',[Variable('?cb','container',ocb),Variable('?p1','pile',op1)]);
    p11=Predicado('in',[Variable('?cc','container',occ),Variable('?p1','pile',op1)]);
    p12=Predicado('in',[Variable('?cd','container',ocd),Variable('?q1','pile',oq1)]);
    p13=Predicado('in',[Variable('?ce','container',oce),Variable('?q1','pile',oq1)]);
    p14=Predicado('in',[Variable('?cf','container',ocf),Variable('?q1','pile',oq1)]);    
   
    p15=Predicado('on',[Variable('?ca','container',oca),Variable('?pallet','container',opallet)])
    p16=Predicado('on',[Variable('?cb','container',ocb),Variable('?ca','container',oca)])
    p17=Predicado('on',[Variable('?cc','container',occ),Variable('?cb','container',ocb)])
    
    p18=Predicado('on',[Variable('?cd','container',ocd),Variable('?pallet','container',opallet)])
    p19=Predicado('on',[Variable('?ce','container',oce),Variable('?cd','container',ocd)])
    p20=Predicado('on',[Variable('?cf','container',ocf),Variable('?ce','container',oce)])

    p21=Predicado('top',[Variable('?cc','container',occ),Variable('?p1','pile',op1)]);
    p22=Predicado('top',[Variable('?cf','container',ocf),Variable('?q1','pile',oq1)]);
    p23=Predicado('top',[Variable('?pallet','container',opallet),Variable('?p2','pile',op2)]);
    p24=Predicado('top',[Variable('?pallet','container',opallet),Variable('?q2','pile',oq2)]);
   
    p25=Predicado('at',[Variable('?r1','robot',or1),Variable('?l1','location',ol1)]);
    p26=Predicado('unloaded',[Variable('?r1','robot',or1)]);
    p27=Predicado('occupied',[Variable('?l1','location',ol1)]);
    
    p28=Predicado('empty',[Variable('?k1','location',ok1)])
    p29=Predicado('empty',[Variable('?k2','location',ok2)])
    
    p30=Predicado('in',[Variable('?ca','co ntainer',oca),Variable('?p2','pile',op2)]);
    p31=Predicado('in',[Variable('?cb','container',ocb),Variable('?q2','pile',oq2)]);
    p32=Predicado('in',[Variable('?cc','container',occ),Variable('?p2','pile',op2)]);
    p33=Predicado('in',[Variable('?cd','container',ocd),Variable('?q2','pile',oq2)]);
    p34=Predicado('in',[Variable('?ce','container',oce),Variable('?q2','pile',oq2)]);
    p35=Predicado('in',[Variable('?cf','container',ocf),Variable('?q2','pile',oq2)]);
 
    objetos=[or1,ol1,ol2,ok1,ok2,op1,oq1,op2,oq2,oca,ocb,occ,ocd,oce,ocf,opallet] 
    mundo = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29]
    resultado=[p30,p31,p32,p33,p34,p35]
    problema=Problema('dw',dominio,objetos,mundo,resultado)

    print(problema)
    print(dominio)
    raiz = Nodo([],None,True)

    b=combinaciones(take,problema)
    print(len(b))          
    
    com = b[1]
   
    
    for predicado in  take.precondiciones: 
       variables=set()  
       
       for y in com:
           if (mismo_tipo(y,predicado.variables)):
               variables.add(y)

       lista_temp=list(variables)
       
       """
       Tengo que checar si esta en el mundo
       el predicado con estos objetos
       """
    """
       print predicado 
       for variable in variables:
          print variable

       print "\n"               
    """ 
    """print Predicado(predicado.nombre,variables,predicado.negativo)"""
    """Para el punto dos necesitan, para cada acción, crear una lista de parámetros y variables
    (pueden tratarlas como lo mismo) y, dados sus tipos, determinar todos los objetos del dominio
    que podrían ser asignados a cada una de esas variables. """
    """
    Para cada combinación posible de asignaciones,
    deben recorrer los predicados uno por uno, realizando las sustituciones de las variables por los
    objetos en esa asignación y revisar si el predicado aterrizado correspondiente está en el dominio.
    Si no está, descartan esa asignación, si sí está continúan con el siguiente predicado. Si logran
    revisar todos los predicados con una asignación, quiere decir que esa acción, con esa 
    sustitución define una acción aplicable. Encuentren todas las acciones con sus sustituciones que son
    aplicables dada una descripción del dominio."""