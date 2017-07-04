/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ia;

import processing.core.PApplet;
import processing.core.PFont;
import java.util.Random;
import java.util.Stack;

/**
 *
 * @author blackzafiro
 */
public class Laberinto extends PApplet {

    PFont fuente= createFont("Arial",12,true);;  // Fuente para mostrar texto en pantalla
    
    // Propiedades del modelo del Laberinto.
    int alto = 30;           // Altura (en celdas) de la cuadricula.
    int ancho =30;           // Anchura (en celdas) de la cuadricula.
    int celda =25;           // Tamanio de cada celda cuadrada (en pixeles).
    ModeloLaberinto modelo;   // El objeto que representa el modelo de termitas.

   
    @Override
    public void setup() {
        frameRate(60);
        size(ancho*celda,alto*celda);
        background(50);
        modelo = new ModeloLaberinto(ancho, alto, celda);
          /**Inicializo la cuadrícula pinto los cuadros del fondo de la cuadrícuña de color blanco*/  
     for(int i = 0; i < alto; i++)
          for(int j = 0; j < ancho; j++){
              //Instrucciones para rellenar el cuadro de blanco
              noStroke();
              fill(255,255,255);  
              rect(j*modelo.tamanio, i*modelo.tamanio, modelo.tamanio, modelo.tamanio);
              
              //Instrucciones para pintar las lineas
              stroke(0,0,0);
              fill(255,255,255);  
	      line(j*modelo.tamanio ,i*modelo.tamanio,(j+1)*modelo.tamanio ,i*modelo.tamanio );
              line(j*modelo.tamanio ,i*modelo.tamanio,j*modelo.tamanio ,(i+1)*modelo.tamanio-1);
       }
              
 
         Agente a = new Agente(modelo.rnd.nextInt(ancho),modelo.rnd.nextInt(alto),modelo.rnd.nextInt(4),null);
         modelo.celda.push(a);
         modelo.mundo[a.posY][a.posX]=true;
    }
    
 
    
    /**Método para quitar la pared correct
     * @param Agente*/
    public void quitaPared(Agente t){
        stroke(255,255,255);
        switch(t.pared){
            case 0:
            //pinta la linea de arriba
     	    line((t.posX)*modelo.tamanio ,(t.posY)*modelo.tamanio,(t.posX+1)*modelo.tamanio ,(t.posY)*modelo.tamanio );
             //pinta la linea de la izquierda
	    line((t.posX)*modelo.tamanio ,(t.posY)*modelo.tamanio,(t.posX)*modelo.tamanio ,(t.posY+1)*modelo.tamanio);
             //pinta la linea de la derecha
	    line((t.posX+1)*modelo.tamanio ,(t.posY)*modelo.tamanio,(t.posX+1)*modelo.tamanio ,(t.posY+1)*modelo.tamanio );
            break;    
            case 1:
            //pinta la linea de arriba
     	    line((t.posX)*modelo.tamanio ,(t.posY)*modelo.tamanio,(t.posX+1)*modelo.tamanio ,(t.posY)*modelo.tamanio );
            //pinta la linea de abajo
	    line((t.posX)*modelo.tamanio ,(t.posY+1)*modelo.tamanio,(t.posX+1)*modelo.tamanio ,(t.posY+1)*modelo.tamanio );
             //pinta la linea de la derecha
	    line((t.posX+1)*modelo.tamanio ,(t.posY)*modelo.tamanio,(t.posX+1)*modelo.tamanio ,(t.posY+1)*modelo.tamanio );
            break;  
            case 2:
            //pinta la linea de abajo
	    line((t.posX)*modelo.tamanio ,(t.posY+1)*modelo.tamanio,(t.posX+1)*modelo.tamanio ,(t.posY+1)*modelo.tamanio );
             //pinta la linea de la izquierda
	    line((t.posX)*modelo.tamanio ,(t.posY)*modelo.tamanio,(t.posX)*modelo.tamanio ,(t.posY+1)*modelo.tamanio);
             //pinta la linea de la derecha
	    line((t.posX+1)*modelo.tamanio ,(t.posY)*modelo.tamanio,(t.posX+1)*modelo.tamanio ,(t.posY+1)*modelo.tamanio );
            break;    
            case 3:
            //pinta la linea de arriba
     	    line((t.posX)*modelo.tamanio ,(t.posY)*modelo.tamanio,(t.posX+1)*modelo.tamanio ,(t.posY)*modelo.tamanio );
            //pinta la linea de abajo
	    line((t.posX)*modelo.tamanio ,(t.posY+1)*modelo.tamanio,(t.posX+1)*modelo.tamanio ,(t.posY+1)*modelo.tamanio );
             //pinta la linea de la izquierda
	    line((t.posX)*modelo.tamanio ,(t.posY)*modelo.tamanio,(t.posX)*modelo.tamanio ,(t.posY+1)*modelo.tamanio);
            break;    
        }
     
    }
    /**
     * Pintar el mundo del modelo 
     */
    @Override
    public void draw() {
      modelo.BackTrack();
    }
   
   
    
    
    
    // --- Clase Agente ---
    /**
     * Representa cada una de las termitas del modelo.
     */
    class Agente{
      int posX, posY,direccion,pared;  // Posicion direccion y pared de la termita
      Agente anterior; //Agente anterior se usa para pintar 
      
      
      /** Constructor de un agente
        @param posX Indica su posicion en el eje X
        @param posX Indica su posicion en el eje Y
        @param direccion Indica la direccion en la que mira.
        @param Agente Indica el agente anterior 
            -----------
           |   | 0 |   |
           |-----------|
           | 3 |   | 1 |
           |-----------|
           |   | 2 |   |
            -----------
      */
      
      Agente(int posX, int posY, int direccion,Agente anterior){
        this.posX = posX;
        this.posY = posY;
        this.direccion = direccion;
        this.anterior=anterior;
      }

       
    }

    

   
    /**
     Representa el laberinto
     */
    class ModeloLaberinto{
      int ancho, alto;               // Tamaño de celdas a lo largo y ancho de la cuadrícula.
      int tamanio;                   // Tamaño en pixeles de cada celda.
      Boolean [][] mundo;            // Mundo de celdas donde habitan las astillas.
      Agente termitas;    // Todas las termitas del modelo.
      Random rnd = new Random();      // Auxiliar para decisiones aleatorias.
      Stack<Agente> celda;            //Stack usado en el backtracking
      /** Constructor del modelo
        @param ancho Cantidad de celdas a lo ancho en la cuadricula.
        @param ancho Cantidad de celdas a lo largo en la cuadricula.
        @param tamanio Tamaño (en pixeles) de cada celda cuadrada que compone la cuadricula.

      */
      ModeloLaberinto(int ancho, int alto, int tamanio){
        this.ancho = ancho;
        this.alto = alto;
        this.tamanio = tamanio;
        
        mundo = new Boolean [alto][ancho];
        for(int i = 0; i < alto; i++)
          for(int j = 0; j < ancho; j++)
            mundo[i][j] = false;
     
        
        termitas=(new Agente(rnd.nextInt(ancho), rnd.nextInt(alto), rnd.nextInt(8),null));
        celda=new Stack<>();
      }

      public void BackTrack(){
       
       if(celda.isEmpty()){
       return ;
       }
      
       Agente a = celda.pop();
       if(yaNoTieneSalida(a)){
       return;
       }
       
       Agente aux=sePuedeMover(a,true);
          if(aux!=null){
            celda.push(a);
            moverAgente(a,a.direccion);
            celda.push(aux);
          }else{
            a.direccion=rnd.nextInt(4);
            celda.push(a); 
           }
        
      }
      /** Mueve un Agente segun la direccion dada.
        Considerando que las fronteras son periodicas.
        @param t La termita a mover en el modelo.
        @param direccion La direccion en la que se desea mover la termita (con valor entre 0 y 7).
      */
      Agente moverAgente(Agente aux, int direccion){
          direccion=direccion%4;     
         Agente t=new Agente(aux.posX,aux.posY,direccion,aux);
          switch(direccion){
          case 0:  t.posY = (t.posY-1)<0?t.posY:(t.posY-1);
                   t.pared=0;
                   break;
          case 1:  t.posX = (t.posX+1)<ancho?(t.posX+1):t.posX;
                   t.pared=1;
                   break;
          case 2:  t.posY = (t.posY+1)<alto?(t.posY+1):t.posY;
                   t.pared=2;
                   break;
          case 3:  t.posX = (t.posX-1)<0?t.posX:(t.posX-1);
                   t.pared=3;
                   break;
        }
          
          
          if(t.anterior!=null){
            noStroke();
            fill(255,0,0);  
            rect(t.anterior.posX*modelo.tamanio, t.anterior.posY*modelo.tamanio, modelo.tamanio, modelo.tamanio);   
            quitaPared(t);    
          }
          
            fill(0, 0, 255);
            noStroke();
            rect(t.posX*modelo.tamanio, t.posY*modelo.tamanio, modelo.tamanio, modelo.tamanio);
          
           t.direccion = rnd.nextInt(4);
           mundo[t.posY][t.posX]=true;    
           return t;
      }
    
      
         Agente moverAgente2(Agente aux, int direccion){
          direccion=direccion%4;     
          Agente t=new Agente(aux.posX,aux.posY,aux.direccion,aux.anterior);
         switch(direccion){
          case 0:  t.posY = (t.posY-1)<0?t.posY:(t.posY-1);
                   t.pared=0;
                   break;
          case 1:  t.posX = (t.posX+1)<ancho?(t.posX+1):t.posX;
                   t.pared=1;
                   break;
          case 2:  t.posY = (t.posY+1)<alto?(t.posY+1):t.posY;
                   t.pared=2;
                   break;
          case 3:  t.posX = (t.posX-1)<0?t.posX:(t.posX-1);
                   t.pared=3;
                   break;
        }       
        return t;
      }
      
     
      
    /**Te dice si un agente ya no tiene salida*/
      private boolean yaNoTieneSalida(Agente a){
      return sePuedeMover(new Agente(a.posX,a.posY,0,a),false)==null&&
             sePuedeMover(new Agente(a.posX,a.posY,1,a),false)==null&&
             sePuedeMover(new Agente(a.posX,a.posY,2,a),false)==null&&
             sePuedeMover(new Agente(a.posX,a.posY,3,a),false)==null;
      }
      
      /**Te dice si un agente se puede mover en la direccion indicada*/
      private Agente sePuedeMover(Agente a,boolean u) {
          Agente aux = moverAgente2(a,a.direccion);
           if(aux.posX==a.posX&&aux.posY==a.posY)
           return null;
           else if(mundo[aux.posY][aux.posX])
           return null;
           if(u){  
           return moverAgente(a,a.direccion);}
           return aux;
       }
        
   

    }
    
    static public void main(String args[]) {
        PApplet.main(new String[] { "ia.Laberinto" });
    }
}
