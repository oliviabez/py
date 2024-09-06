#COMPONENTES: Maria antônia, Lívia Maria, Nicolle Evelyn e Olívia Bezerra
#TURMA: Info1m
#DISCIPLINA: Introdução a Programação

print("Bem-Vindo ao quiz interativo")
user=input("Digite (sim) para contiuar! \n Aperte enter no final da resposta! \n :")

if user!="sim":
    quit()
    
score=0 #somando pontos

print("Começando...")

print()

print("Menu de Opções")
print("1.Matemática")
print("2.Introdução a Programação")
print("3.Geografia")
print("4.Sair")
 

print()

escolha=input("Escolha qual quiz você deseja fazer \n Ou 4 para sair:")

if escolha=="4":
    print("Saindo...")
    quit()

print()

#quiz 01
if escolha=="1":
    print("Questão 1- Qual é a raiz quadrada do número 64? \n a)6\n b)8 \n c)18 \n d)4")
    opcao=input("Digite uma das alternativas:")
    
    print()
    
    if(opcao=="b"):
        print("Alternativa correta!")
        score=score+10
        
        print()
        
    elif(opcao!="b"):
        print("Alternativa incorreta :( \n Alternativa Correta, letra B")
        
        print()
        
if escolha=="1":   
    print("Questão 2- Se em uma conta de banco tinha R$500,00 e foram retirados R$240,00. Quanto restou na conta? \n a)350 \n b)200 \n c)410 \n d)260 ")
    opcao=input("Digite uma das alternativas:")
    
    print()
    
    if(opcao=="d"):
        print("Alternativa correta!")
        score=score+10
        
        print()
        
    elif(opcao!="d"):
        print("Alternativa incorreta :( \n Alternativa correta, letra D")
        
    print()
    
if escolha=="1":
     print("Questão 3- Qual o valor de 2500 dividido para 50? \n a)150 \n b)100 \n c)50 \n d)250")
     opcao=input("Digite uma das alternativas:")
     score=score+10
     
     print()
    
if(opcao=="c"):
        print("Alternativa correta!")
        score=score+10
        print()
        
elif(opcao!="c"):
        print("Alternativa incorreta :( \n Alternativa Correta, letra C")
        
        print()
    
if escolha=="1":
    print("Questão 4- Qual o valor do produto entre 560 e 90? \n a)50.400 \n b)40.000 \n c)65.500 \n d)55.660")
    opcao=input("Digite uma das alternativas:")
    
    print()
    
    if(opcao=="a"):
        print("Alternativa correta!")
        score=score+10
        print()
        
    elif(opcao!="a"):
        print("Alternativa incorreta :( \n Alternativa Correta, letra A")
    
    valor_medido = score
    valor_verdadeiro = 50

        # Calcula o erro absoluto
    erro_absoluto = abs(valor_medido - valor_verdadeiro)
        
        # Calcula o percentual de erro
    percentual_erro = (erro_absoluto / valor_verdadeiro) * 100
    print(f"O percentual de erro é: {percentual_erro:.2f}%")
print()
    
numero_acertos = score
numero_tentativas = 50

percentual_acertos = (numero_acertos / numero_tentativas) * 100
print(f"Percentual de Acertos: {percentual_acertos:.2f}%")

        
cont=input("Quer continuar? \n Aperte enter no final da resposta (sim/não)")
if cont!="sim":
   quit()
    
print("Menu de Opções")
print("1.Matemática")
print("2.Introdução a Programação")
print("3.Geografia")
print("4.Sair")
  
if escolha=="4":
        print("Saindo...")
quit()

#quiz 02
if escolha=="2":
    print("Questão 1- Qual o comando usado para exibir informações na tela? \n a)if \n b)print \n c)else \n d)input")
    opcao=input("Digite uma das alternativas:")
    
    print()
    
    if(opcao=="b"):
        print("Alternativa correta!") 
        score=score+10
        
        print()
         
    elif(opcao!="b"):
        print("Alternativa incorreta :( \n Alternativa correta, letra B") 
        
    print()
    
if escolha=="2":    
    print("Questão 2- Para quê serve a memória de um computador? \n a)Armazenar Dados \n b)Organizar Pastas \n c)Enviar mensagens \n d)Todas as alternativas")
    opcao=input("Digite uma das alternativas:")
    
    print()
    
    if(opcao=="a"):
        print("Alternativa correta!")
        score=score+10
        
        print()
        
    elif(opcao!="a"):
        print("Alternativa incorreta :( \n Alternativa Correta, letra A")
 
    print()
    
if escolha=="2":   
    print("Questão 3- O que são variáveis?\n a)Espaço reservado na memória do computador \n b)Um determinado valor fixo \n c) Tipos de atribuição \n d)Tipos de dados")
    opcao=input("Digite uma das alternativas:")
    
    print()
    
    if(opcao=="a"):
        print("Alternativa correta!")
        score=score+10
        
        print()
        
    elif(opcao!="a"):
        print("Alternativa incorreta :( \n Alternativa Correta, letra A")
        
    print()
    
if escolha=="2": 
    print("Questão 4- Quais são os operadores usados no programa python? \n a)Aritméticos,lógicos,abstração \n b)Relacionais,pensamento computacional,algoritmo \n c)Algoritmo,abstração,relacionais \n d)Relacionais,aritméticos,lógicos")
    opcao=input("Digite uma das alternativas:")
    
    print()
    
    valor_medido = score
    valor_verdadeiro = 50

        # Calcula o erro absoluto
    erro_absoluto = abs(valor_medido - valor_verdadeiro)
        
        # Calcula o percentual de erro
    percentual_erro = (erro_absoluto / valor_verdadeiro) * 100
    print(f"O percentual de erro é: {percentual_erro:.2f}%")
print()
    
numero_acertos = score
numero_tentativas = 50

percentual_acertos = (numero_acertos / numero_tentativas) * 100
print(f"Percentual de Acertos: {percentual_acertos:.2f}%")
    
print()
    
if(opcao=="d"):
        print("Alternativa correta!")
        score=score+10
        
        print()
        
elif(opcao!="d"):
        print("Alternativa incorreta :( \n Alternativa Correta, letra D")
        
        print()
        
 #quiz 03
if escolha=="3":
    print("Questão 1- Quantos continentes existem atualmente? \n a)5 \n b)4 \n c)6 \n d)8")
    opcao=input("Digite uma das alternativas:")
    
    print()
        
    if(opcao=="c"):
        print("Alternativa Correta!")
        score=score+10
        
        print()
        
    elif(opcao!="c"):
        print("Alternativa Incorreta:( \n Alternativa Correta, letra C")
        
        print()
        
if escolha=="3":
    print("Questão 2- Quais são as camadas da Terra? \n a)Núcleo, Manto e Crosta \n b)Crosta, Atmosfera e Núcleo \n c)Manto, Terra e Atmosfera \n d)Núcleo, Troposfera e Estratosfera")
    opcao=input("Digite uma das alternativas:")
    
    if(opcao=="a"):
        print("Alternativa Correta!")
        score=score+10
        
        print()

    elif(opcao!="a"):
        print("Alternativa Incorreta:( \n Alternativa Correta, letra A")
    
        print()

if escolha=="3":
    print("Questão 3- Qual movimento da Terra responsável pelos dias e as noites? \n a)Maritimidade \n b)Translação \n c)Equinócio \n d)Rotação")
    opcao=input("Digite uma das alternativas:")

    if (opcao=="d"):
        print("Alternativa Correta!")
        score=score+10 

        print()

    elif(opcao!="d"):
        print("Alternativa Incorreta:( \n Alternativa Correta, letra D")

        print()

if escolha=="3":
    print("Questão 4- Em qual camada da atmosfera nós estamos inseridos? \n a)Exosfera \n b)Troposfera \n c)Mesosfera \n d)Termosfera")
    opcao=input("Digite uma das alternativas:")

    if (opcao=="b"):
        print("Alternativa Correta!")
        score=score+10
    elif(opcao!="b"):
        print("Alternativa Incorreta:( \n Alternativa Correta, letra B")
    
    valor_medido = score
    valor_verdadeiro = 50

        # Calcula o erro absoluto
    erro_absoluto = abs(valor_medido - valor_verdadeiro)
        
        # Calcula o percentual de erro
    percentual_erro = (erro_absoluto / valor_verdadeiro) * 100
    print(f"O percentual de erro é: {percentual_erro:.2f}%")
    
print()
    
numero_acertos = score
numero_tentativas = 50

percentual_acertos = (numero_acertos / numero_tentativas) * 100
print(f"Percentual de Acertos: {percentual_acertos:.2f}%")
print()

#fim de processo
cont=input("Voltar?... \n Aperte enter no final da resposta (digite sim)")
if cont!="Sim":
    quit()
    
print("Menu de Opções")
print("1.Matemática")
print("2.Introdução a Programação")
print("3.Geografia")
print("4.Sair")

if escolha=="4":
        print("Saindo...")
quit()
