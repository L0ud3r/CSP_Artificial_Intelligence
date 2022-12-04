#class Turma:
#    def __init__(self) -> None:
#        pass

#class Uc:
#    def __init__(self) -> None:
#        pass 
    
#class Sala: 
#    def __init__(self) -> None:
#        pass
    
#class Professor:  
#    def __init__(self) -> None:
#        pass           
    
#class Data: 
#    def __init__(self) -> None:
#        pass       
    
class Aula:
    def __init__(self,turma,uc,sala,dia_semana,duracao,inicioAula):
        self.turma = turma
        self.uc = uc
        self.sala = sala
        self.dia_semana = dia_semana
        self.duracao = duracao
        self.inicioAula = inicioAula
       
    def __str__(self):
        return f"{self.turma},{self.uc},{self.sala},{self.dia_semana},{self.duracao},{self.inicioAula}"
        

     



    
 
    



        