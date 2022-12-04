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