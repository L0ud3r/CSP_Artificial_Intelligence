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
    dominio.update({f'Aula{x}.uc': random.sample(set(range(1, len(uc)+1)),1)})  # disciplina
    dominio.update({f'Aula{x}.dia_semana': set(range(1, 6))})  # Dia semana
    dominio.update({f'Aula{x}.duracao': {2}})  # Tempo de aula
    dominio.update({f'Aula{x}.inicioAula': set(range(9, 18))}) # Inicio até Inicio do ultimo bloco


# Ciclos que percorrem as turmas (fazendo comparação de cada aula entre cada turma)
for x in range(0, len(turma) * 10):
    for y in range(x + 1, len(turma) * 10):
        
       # Evita que para diferentes turmas tenham a mesma uc no mesmo bloco de um determinado dia
        one_uc_per_timeslot = Constraint((f'Aula{x}.uc', f'Aula{y}.uc',
                                          f'Aula{x}.turma', f'Aula{y}.turma',
                                          f'Aula{x}.dia_semana',f'Aula{y}.dia_semana'
                                          ), lambda aulax_uc, aulay_uc,
                                                    aulax_turma, aulay_turma,
                                                    aulax_dia, aulay_dia,:
                                                        
                                (aulax_dia != aulay_dia)
                                if (aulax_uc == aulay_uc and aulax_turma == aulay_turma) else True)

        # Para um slot do horario, em diferentes horarios não pode ter a mesma sala
        one_classroom_per_timeslot = Constraint((f'Aula{x}.sala', f'Aula{y}.sala',
                                                 f'Aula{x}.dia_semana', f'Aula{y}.dia_semana',
                                                 f'Aula{x}.inicioAula', f'Aula{y}.inicioAula',
                                                 f'Aula{x}.duracao', f'Aula{y}.duracao'), 
                                                lambda aulax_sala, aulay_sala,
                                                       aulax_dia, aulay_dia,
                                                       aulax_inicio, aulay_inicio,
                                                       aulax_duracao, aulay_duracao: 
                                                (aulax_inicio >= (aulay_inicio + aulay_duracao) or
                                                aulay_inicio >= (aulax_inicio + aulax_duracao)) 
                                                if (aulax_sala == aulay_sala and aulax_dia == aulay_dia and aulax_sala != 5) else True)
        
        restricoes.append(one_classroom_per_timeslot)

        # Para um slot do horario, em diferentes horarios não pode ter a mesma turma
        one_class_per_timeslot = Constraint((f'Aula{x}.turma', f'Aula{y}.turma',
                                             f'Aula{x}.dia_semana', f'Aula{y}.dia_semana',
                                             f'Aula{x}.inicioAula', f'Aula{y}.inicioAula',
                                             f'Aula{x}.duracao', f'Aula{y}.duracao'), 
                                            lambda aulax_turma, aulay_turma,
                                            aulax_dia, aulay_dia,
                                            aulax_inicio, aulay_inicio,
                                            aulax_duracao, aulay_duracao:
                            (aulax_inicio >= (aulay_inicio + aulay_duracao) or aulay_inicio >= (aulax_inicio + aulax_duracao))
                            if (aulax_turma == aulay_turma and aulax_dia == aulay_dia) else True)
        
        restricoes.append(one_class_per_timeslot)

        # As aulas online não podem ser reservadas imediatamente após uma aula presencial.
        online_class_not_after_presencial_class_after = Constraint((f'Aula{x}.turma', f'Aula{y}.turma',
                                                                    f'Aula{x}.dia_semana', f'Aula{y}.dia_semana', 
                                                                    f'Aula{x}.inicioAula', f'Aula{y}.inicioAula',
                                                                    f'Aula{x}.duracao', f'Aula{x}.sala', f'Aula{y}.sala'), 
                                                                   lambda aulax_turma, aulay_turma,
                                                                    aulax_dia, aulay_dia,
                                                                    aulax_inicio, aulay_inicio,
                                                                    aulax_duracao, aulax_sala,
                                                                    aulay_sala : (aulay_sala != 5)
                                                                   if(aulax_turma == aulay_turma and aulax_dia == aulay_dia and
                                                                      (aulay_inicio == aulax_inicio - aulax_duracao or 
                                                                       aulay_inicio == aulax_inicio + aulax_duracao or
                                                                       aulax_inicio == aulay_inicio - aulax_duracao or
                                                                       aulax_inicio == aulay_inicio + aulax_duracao) and
                                                                      aulax_sala != 5) else True)
        restricoes.append(online_class_not_after_presencial_class_after)

        # As aulas online não podem ser reservadas imediatamente antes de uma aula presencial.
        online_class_not_after_presencial_class_before = Constraint((f'Aula{x}.turma', f'Aula{y}.turma',
                                                                     f'Aula{x}.dia_semana', f'Aula{y}.dia_semana',
                                                                     f'Aula{x}.inicioAula', f'Aula{y}.inicioAula',
                                                                     f'Aula{x}.duracao', f'Aula{x}.sala', f'Aula{y}.sala'),
                                                                    lambda aulax_turma, aulay_turma,
                                                                    aulax_dia, aulay_dia, aulax_inicio,
                                                                    aulay_inicio, aulay_duracao, aulax_sala,
                                                                    aulay_sala : (aulax_sala != 5) 
                                                                    if(aulax_turma == aulay_turma and aulax_dia == aulay_dia and 
                                                                       (aulay_inicio == aulax_inicio - aulay_duracao or
                                                                        aulay_inicio == aulax_inicio + aulay_duracao or
                                                                        aulax_inicio == aulay_inicio - aulay_duracao or
                                                                        aulax_inicio == aulay_inicio + aulay_duracao) and
                                                                       aulay_sala != 5) else True)
        restricoes.append(online_class_not_after_presencial_class_before)

        # Uma turma não deve ter mais de 3 aulas por dia.
        # A solução foi certificar de que as aulas a preencher são 2 horas após a aula X, de forma a que ocupe o horario inteiro e limite assim o numero de aulas diarias
        # As condições são para o caso de ser antes da aulaX ou depois da aulaX
        atmost_three = Constraint((f'Aula{x}.turma', f'Aula{y}.turma',
                                   f'Aula{x}.dia_semana', f'Aula{y}.dia_semana',
                                   f'Aula{x}.inicioAula', f'Aula{y}.inicioAula',
                                   f'Aula{x}.duracao'),
                                  lambda aulax_turma, aulay_turma,
                                         aulax_dia, aulay_dia,
                                         aulax_inicio, aulay_inicio,
                                         aulax_duracao: 
                                  (aulay_inicio <= aulax_inicio and
                                   aulay_inicio >= aulax_inicio - aulax_duracao*2) or
                                  (aulay_inicio >= aulax_inicio and
                                   aulay_inicio <= aulax_inicio + aulax_duracao*2) 
                                                                                                                                                            if(aulax_turma == aulay_turma and aulax_dia == aulay_dia) else True)
        restricoes.append(atmost_three)
                

class_scheduling = NaryCSP(dominio, restricoes)

#region Prints Teste

    # print(class_scheduling.variables)
    # print(class_scheduling.domains)
    # print(class_scheduling.constraints)
    # print("\n\n")
    # print(class_scheduling)

#endregion

print(ac_search_solver(class_scheduling, arc_heuristic=sat_up))
#print(at_least_towfour_in_same_room(dominio,1,{1}))
#print(more_than_2_UC_per_week(dominio,1,1))
#print(more_than_2_UC_per_week(get_only_list_of_attribute_from_class(x, "uc"),turma[1],2,{1}))
