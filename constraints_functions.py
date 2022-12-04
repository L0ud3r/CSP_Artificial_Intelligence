# Verifica se o numero de vezes que uma uc aparece numa determinada turma esta entre 1 e 2
def more_than_2_UC_per_week(dominio, uc, turma):
    counter = 0;

    for x in range(0, 20):
        for y in range(x+1, 20):
            listAuxxUC = dominio[f'Aula{x}.uc']
            listAuxyUC = dominio[f'Aula{y}.uc']
            listAuxxTurma = dominio[f'Aula{x}.turma']
            listAuxyTurma = dominio[f'Aula{y}.turma']

            if ((listAuxxUC[0] == listAuxyUC[0] == uc) and (listAuxxTurma == listAuxyTurma == turma)): counter += 1

    if (counter >= 1 and counter <= 2): return 1

    return 0


# Verifica se o numero de vezes que uma turma tem numa determinada sala esta entre 2 a 4 vezes
def at_least_towfour_in_same_room(dominio, sala, turma):
    counter = 0;
    for x in range(0, 20):
        for y in range(x+1, 20):
            listAuxxSala = dominio[f'Aula{x}.sala']
            listAuxySala = dominio[f'Aula{y}.sala']
            listAuxxTurma = dominio[f'Aula{x}.turma']
            listAuxyTurma = dominio[f'Aula{y}.turma']
            
            if((listAuxxSala == listAuxySala == sala) and (listAuxxTurma == listAuxyTurma == turma)): counter += 1;
    
    if(counter >= 2 and counter <= 4): return 1 
    
    return 0

# Função que retorna uma lista das disciplinas de cada aula da turma passada por parametro
def list_of_uc_of_classes(turma):
    list = []
    
    x = (turma - 1) * 10
    size = turma * 10 - 1
    
    while (x <= size):
        list.append(f'Aula{x}.{"uc"}')
        x += 1
        
    return list

# Função que retorna uma lista dos dias da semana de cada aula da turma passada por parametro
def list_of_weekday_of_classes(turma):
    list = []
    
    x = (turma - 1) * 10
    size = turma * 10 - 1
    
    while (x <= size):
        list.append(f'Aula{x}.{"dia_semana"}')
        x += 1
        
    return list