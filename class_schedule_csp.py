from csp import *
from classes import *
from constraints_functions import *

# region Variaveis

turma = { 1: "a", 2: "b" }

uc = { 1: "matematica", 2: "ciencias", 3: "ingles", 4: "historia" , 5:"aplicacoes informaticas" }

sala = { 1: "201", 2: "202", 3: "104", 4: "108", 5: "online" }

aula_inicial = 0
prox_inicial = 10

aulas = []

# loop para criar as aulas necessárias (10 aulas por turma)
for i in range(len(turma) * 10):
    novaAula = Aula(None, None, None, None, None, None)
    aulas.append(novaAula)

dominio = {}

restricoes = []

# endregion


# Ciclo para atribuição de salas a cada aula, inclusive aulas online, atribuindo esses mesmo valores ao dominio
# Aulas online foram atribuídas logo de início
for turma_atual in turma:
    aulas_online_atuais = 0
    aulas_online_max = 2
    
    while aula_inicial != prox_inicial:
        dominio.update({f'Aula{aula_inicial}.turma': {turma_atual}})
        
        if(aulas_online_atuais < aulas_online_max):
            dominio.update({f'Aula{aula_inicial}.sala': {5}})
        else:
            dominio.update({f'Aula{aula_inicial}.sala': random.sample(set(range(1, len(sala))),1)})
        aulas_online_atuais += 1
        aula_inicial += 1
    aula_inicial = prox_inicial
    prox_inicial += 10


# Ciclo de atribuição de valores ao dominio para disciplina, dia da semana, duracao e hora de inicio de aula
for x, list_enumerate in enumerate(aulas):
    dominio.update({f'Aula{x}.uc': set(range(1, len(uc)+1))})  # disciplina
    dominio.update({f'Aula{x}.dia_semana': set(range(1, 6))})  # Dia semana
    dominio.update({f'Aula{x}.duracao': {2}})  # Tempo de aula
    dominio.update({f'Aula{x}.inicioAula': set(range(9, 18))}) # Inicio até Inicio do ultimo bloco


# Ciclos que percorrem as turmas (fazendo comparação de cada aula entre cada turma)
for x in range(0, len(turma) * 10):
    for y in range(x + 1, len(turma) * 10):
        # Para um slot do horario, não pode ter a mesma uc na mesma turma
        one_uc_per_timeslot = Constraint((f'Aula{x}.uc', f'Aula{y}.uc',
                                          f'Aula{x}.turma', f'Aula{y}.turma',
                                          f'Aula{x}.dia_semana',f'Aula{y}.dia_semana'
                                          ), lambda aulax_uc, aulay_uc,
                                                    aulax_turma, aulay_turma,
                                                    aulax_dia, aulay_dia,:
                                                        
                                (aulax_dia != aulay_dia)
                                if (aulax_uc == aulay_uc and aulax_turma == aulay_turma) else True)

        restricoes.append(one_uc_per_timeslot)

        # Para um slot do horario, não pode ter a mesma sala
        one_classroom_per_timeslot = Constraint((f'Aula{x}.sala', f'Aula{y}.sala',
                                                f'Aula{x}.dia_semana',f'Aula{y}.dia_semana',
                                                f'Aula{x}.duracao',f'Aula{y}.duracao',
                                                f'Aula{x}.inicioAula',f'Aula{y}.inicioAula',
                                                ), lambda aulax_sala, aulay_sala,
                                                          aulax_dia, aulay_dia, 
                                                          aulax_duracao, aulay_duracao,
                                                          aulax_inicio, aulay_inicio:
                                                              
                                (aulax_inicio >= (aulay_inicio + aulay_duracao) or aulay_inicio >= (aulax_inicio + aulax_duracao))
                                if (aulax_sala != 5 and aulax_sala == aulay_sala and aulax_dia == aulay_dia) else True)
        
        restricoes.append(one_classroom_per_timeslot)
        
        # Para um slot do horario, não pode ter a mesma turma
        one_class_per_timeslot = Constraint((f'Aula{x}.turma', f'Aula{y}.turma',
                                            f'Aula{x}.dia_semana',f'Aula{y}.dia_semana',
                                            f'Aula{x}.duracao',f'Aula{y}.duracao',
                                            f'Aula{x}.inicioAula',f'Aula{y}.inicioAula'
                                            ), lambda aulax_turma, aulay_turma,
                                                      aulax_dia, aulay_dia, 
                                                      aulax_duracao, aulay_duracao,
                                                      aulax_inicio, aulay_inicio: 
                                                          
                                (aulax_inicio >= (aulay_inicio + aulay_duracao) or aulay_inicio >= (aulax_inicio + aulax_duracao))
                                if (aulax_turma == aulay_turma and aulax_dia == aulay_dia) else True)
        
        restricoes.append(one_class_per_timeslot)
        
        # Aulas online não podem ser seguidas de aulas presenciais
        # Foram feitas 2 constraints para o caso de ser uma aula antes 
        # ou depois da aula a ser verificada atualmente
        online_presencial_class_problem_x = Constraint((f'Aula{x}.turma', f'Aula{y}.turma',
                                                        f'Aula{x}.dia_semana',f'Aula{y}.dia_semana',
                                                        f'Aula{x}.sala',f'Aula{y}.sala',
                                                        f'Aula{x}.duracao',f'Aula{y}.duracao',
                                                        f'Aula{x}.inicioAula',f'Aula{y}.inicioAula',
                                                        ), lambda aulax_turma, aulay_turma,
                                                                  aulax_dia, aulay_dia, 
                                                                  aulax_sala, aulay_sala,
                                                                  aulax_duracao, aulay_duracao,
                                                                  aulax_inicio, aulay_inicio:
                                
                                (aulax_sala != 5)
                                if (aulax_turma == aulay_turma and aulax_dia == aulay_dia and 
                                    (aulay_inicio == aulax_inicio - aulax_duracao or 
                                    aulay_inicio == aulax_inicio + aulax_duracao or 
                                    aulax_inicio == aulay_inicio - aulay_duracao or 
                                    aulax_inicio == aulay_inicio + aulay_duracao) and 
                                    aulay_sala != 5) else True)
        
        restricoes.append(online_presencial_class_problem_x)
        
        online_presencial_class_problem_y = Constraint((f'Aula{x}.turma', f'Aula{y}.turma',
                                                        f'Aula{x}.dia_semana',f'Aula{y}.dia_semana',
                                                        f'Aula{x}.sala',f'Aula{y}.sala',
                                                        f'Aula{x}.duracao',f'Aula{y}.duracao',
                                                        f'Aula{x}.inicioAula',f'Aula{y}.inicioAula',
                                                        ), lambda aulax_turma, aulay_turma,
                                                        aulax_dia, aulay_dia, 
                                                        aulax_sala, aulay_sala,
                                                        aulax_duracao, aulay_duracao,
                                                        aulax_inicio, aulay_inicio:
                                            
                                (aulay_sala != 5)
                                if (aulax_turma == aulay_turma and aulax_dia == aulay_dia and 
                                    (aulay_inicio == aulax_inicio - aulax_duracao or 
                                    aulay_inicio == aulax_inicio + aulax_duracao or 
                                    aulax_inicio == aulay_inicio - aulay_duracao or 
                                    aulax_inicio == aulay_inicio + aulay_duracao) and 
                                    aulax_sala != 5) else True)
        
        restricoes.append(online_presencial_class_problem_y)
                

# Verifica se uma uc aparece 2 vezes por semana
def two_lessons_uc_per_schedule(*list):
    # Percorre as UCs de cada aula
    for x in uc:
        # Caso o número de vezes que uma disciplina apareça num horário seja diferente de 2
        if (list.count(x) != 2):
            return False
    return True

# Verifica se tem mais de 3 aulas por dia
def three_lessons_per_day(*list):
    # Percorre os dias da semana
    for x in range(1,6):
        # Caso o dia apareça mais que 3 vezes no horário
        if (list.count(x) > 3):
            return False
    return True

# restrições que ocorrerão em cada horário (ou seja em cada turma)
for x in turma:
    # Uma disciplina só pode ser lecionada 2 vezes por semana
    # Neste caso é criada uma lista (tuple, tendo em conta os argumentos de Constraint()) com as UCs de cada aula por nodo
    # Esta lista é usada na função chamada no parâmetro seguito, o mesmo acontece na constraint seguinte
    uc_twice_per_week = Constraint(tuple(list_of_uc_of_classes(x)), two_lessons_uc_per_schedule)
    
    restricoes.append(uc_twice_per_week)
    
    # Só pode haver um máximo de 3 aulas por dia
    max_three_lessons_per_day = Constraint(tuple(list_of_weekday_of_classes(x)), three_lessons_per_day)
    
    restricoes.append(max_three_lessons_per_day)

#region Prints Teste

    # print(class_scheduling.variables)
    # print(class_scheduling.domains)
    # print(class_scheduling.constraints)
    # print("\n\n")
    # print(class_scheduling)

#endregion

# Pesquisa CSP e printagem de estado final atingido
class_scheduling = NaryCSP(dominio, restricoes)
print(ac_solver(class_scheduling, arc_heuristic=sat_up))
#print(ac_search_solver(class_scheduling, arc_heuristic=sat_up))
#print(at_least_towfour_in_same_room(dominio,1,{1}))
#print(more_than_2_UC_per_week(dominio,1,1))
#print(more_than_2_UC_per_week(get_only_list_of_attribute_from_class(x, "uc"),turma[1],2,{1}))
