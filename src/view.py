"""TREES GEN FOR README"""
# Versão 1.0 alpha
# Autor: Yann Escobar
# Data: 16/10/2026
# Todos os direitos reservados

import PySimpleGUI as sg
# Importa a biblioteca PySimpleGUI

from treegen import *

import os


"""Auto explicativo layout da página"""
layout0 = [
    # Futura implementação de abas:
    #[sg.TabGroup([[sg.Tab('tab0', [[sg.T(s=(15,2))]]),
    #               sg.Tab('tab1', [[sg.T()]])
    #               ]])],

    # LAYOUT LEGADO:
    #[sg.Text("Qual o diretório?")], #Primeira seção da janela
    #[sg.InputText(size=40, enable_events=True, key='-ENTRADA-'), sg.FolderBrowse("Procure", target='-ENTRADA-')], #Segunda seção da janela etc...
    # Cria uma caixa para inserir texto, define o tamanho, seta os eventos como True (pode receber eventos)
    # Atribui uma chave chamada '-ENTRADA-'
    
    #[sg.Button("Gerar"), sg.Button("Limpar"), sg.Button("Cancelar")],
    [sg.Text("Bem-vindo ao TreeGen", key='-TEXTOLEGAL-'), sg.Button("Limpar Árvore")],
    [sg.Multiline(default_text="Sua árvore vai aparecer aqui!", pad=(16, 6), key='-OUT-', size=(90, 18), expand_x=False, expand_y=False)],
    [sg.Button("Copiar", size=(15, 1))],
    [sg.HorizontalSeparator(thickness = 3, color='green')], # Usar a cor dele como feedback visual de progressão
    [sg.Text("Qual o diretório?", font=('Courier', 12, 'bold'))],
    [sg.InputText(size=40, enable_events=True, key='-ENTRADA-'), sg.FolderBrowse("Procure", target='-ENTRADA-')],
    [sg.Button("Gerar", size=(15, 1)), sg.Button("Limpar", size=(15, 1)), sg.Button("Sair")],
]

"""Layout do avançado"""
layout1 = [
    # ⚙️
    [sg.Text("Aqui vão ficar as configurações avançadas!")],

    [sg.HorizontalSeparator(thickness = 3, color='green')],

    [sg.Text("Modo de Salvamento:", font=('Arial', 10, 'bold'))],

    [
            sg.Radio("Apenas no App (não salvar)", 'modo_salva', 
                key='-MODO-APP-', default=True),
            sg.Radio("Pasta padrão (/Arvores)", 'modo_salva', 
                key='-MODO-PADRAO-'),
            sg.Radio("Pasta personalizada", 'modo_salva', 
                key='-MODO-CUSTOM-')
    ],


    # Opções de formato
    [sg.Text("Salvar como:", font=('Arial', 10, 'bold'))],
    [sg.Radio("Apenas no App", 
              'formato', key='-FORMATO-APP-', default=True),
     sg.Radio(".txt", 
              'formato', key='-FORMATO-TXT-'),
     sg.Radio(".md", 
              'formato', key='-FORMATO-MD-')
    ],

    # Onde vai ser salvo?
    [sg.Text("Selecione para onde vai a sua árvore:", font=('Arial', 10, 'bold'))],
    [sg.InputText(size=(35, 25), expand_x= True, enable_events=True, key='-NEWOUT-'),
      sg.FolderBrowse("Procurar", target='-NEWOUT-')
    ],
    [sg.Button("Confirmar Pasta", size=(15, 1))],

    # Status legado [sg.Text("", key='-TEXTOSTATUS-')],

    # STATUS atuais
    [sg.Text("Status Atual:", font=('Arial', 10, 'bold'))],
    [sg.Multiline(size=(80, 10), 
                      key='-STATUS-DETALHADO-',
                      expand_x=True,
                      expand_y=True,
                      disabled=True,
                      font=('Courier', 9))],
]


"""Vai juntar os layouts anteriores em um grupo de abas"""
layouts = [
    [sg.TabGroup
    (
        [
            [
             sg.Tab("Gerar", layout0, element_justification='center'),
             sg.Tab("Avançado", layout1),
            ]
        ], key='-TABGROUP-'
    )
    ],
    [sg.Text("Ver 1.0 alpha")]
]

# ===============================================================

"""Seção 'window' constrói a janela"""
window = sg.Window("TreeGen", layouts, resizable=True, size=(600, 535), finalize=True)

#Enquanto condição for verdadeira faça
while True:
    """Condição base para matar o programa"""
    event, values = window.read()
    # A cada ciclo de operação o programa vai salvar os eventos no 'event' paralelamente no 'values'
    # click's do mouse entre outros

    if event == sg.WINDOW_CLOSED or event == "Sair":
        # Ação da biblioteca sg de clicar no botão 'x' da janela
        break

    if event == "Gerar":
        valor_digitado = values["-ENTRADA-"]

        # Verifica se o campo está vago
        if not valor_digitado.strip():
            window["-TEXTOLEGAL-"].update("Digite um caminho")
            continue
        
        # Verifica se o caminho existe mesmo ou é fic kkkkk
        if not os.path.exists(valor_digitado):
            window["-TEXTOLEGAL-"].update("Desculpe esse caminho não existe! Verifique a ortografia e tente de novo.")
            print(f"Debug: não foi possível acessar o diretório {valor_digitado}")
            continue
        
        # Verifica se realmente é uma pasta 
        if not os.path.isdir(valor_digitado):
            window["-TEXTOLEGAL-"].update(f"{valor_digitado} Não é uma pasta, tente de novo!")
            continue

        #DEBUG
        print(f"DEBUG: valor_digitado = '{valor_digitado}'")
        print(f"DEBUG: type = {type(valor_digitado)}")

        resultado = gerar_arvore_diretorios(valor_digitado)
        
        #DEBUG
        print(f"DEBUG: resultado = \n{resultado[:100]}...")  # Mostra os primeiros 100 caracteres
        
        window["-TEXTOLEGAL-"].update(f"Gerando árvore para o projeto {valor_digitado}")

        window["-OUT-"].update(resultado)
        window["-TEXTOLEGAL-"].update(f"Árvore gerada!")
       
        # ← NOVA LÓGICA DE SALVAMENTO:
        # Verifica qual modo foi selecionado
        if values['-MODO-APP-']:
            config['modo_salva'] = 'app'
            window['-STATUS-DETALHADO-'].update("✅ Árvore exibida no app (não salva em arquivo)")

        elif values['-MODO-PADRAO-']:
            config['modo_salva'] = 'padrao'
            pasta_padrao = "./Arvores"
            
            # Cria a pasta se não existir
            if not os.path.exists(pasta_padrao):
                try:
                    os.makedirs(pasta_padrao)
                except Exception as e:
                    window['-STATUS-DETALHADO-'].update(f"❌ Erro ao criar pasta: {str(e)}")
                    continue
            
            # Salva na pasta padrão
            sucesso, mensagem = salvar_arquivo(
                resultado,
                pasta_padrao,
                config['formato_selecionado']
            )
            config['ultima_arvore'] = resultado
            window['-STATUS-DETALHADO-'].update(mensagem)
        
        elif values['-MODO-CUSTOM-']:
            config['modo_salva'] = 'custom'
            
            if not config['pasta_custom']:
                window['-STATUS-DETALHADO-'].update("⚠️ Configure a pasta personalizada primeiro!")
                continue
            
            sucesso, mensagem = salvar_arquivo(
                resultado,
                config['pasta_custom'],
                config['formato_selecionado']
            )
            config['ultima_arvore'] = resultado
            window['-STATUS-DETALHADO-'].update(mensagem)
        #if config['pasta_saida']:  # Se uma pasta de saída foi configurada
        #    sucesso, mensagem = salvar_arquivo(
        #        resultado,
        #        config['pasta_saida'],
        #        config['formato_selecionado']
        #)


    if event == "Limpar":
        valor_digitado = values["-ENTRADA-"]

        if not valor_digitado.strip():
            window["-TEXTOLEGAL-"].update("Nada para limpar!")
            continue
        else:
            window["-ENTRADA-"].update("") # Limpa a entrada do usuário

    if event == "Limpar Árvore":
        valor_resultado = values["-OUT-"]

        if not valor_resultado.strip():
            window["-TEXTOLEGAL-"].update("As árvores não somos nozes!")
            continue
        else:
            window["-OUT-"].update("")
            window["-TEXTOLEGAL-"].update("Eu vou derrubar todas aquelas árvores do iberabuera, brr")

    if event == "Copiar":
        árvoreSaida = values['-OUT-']
        if árvoreSaida.rstrip():
            window.TKroot.clipboard_clear()
            window.TKroot.clipboard_append(árvoreSaida)
            sg.popup_quick_message("A sua árvore foi copiada, para sua área de transferência", auto_close_duration=0.8)
        else:
            sg.popup_error("Você não plantou nenhuma árvore :(")

    if event == "Confirmar Pasta":
        pasDig = values["-NEWOUT-"].strip()

        if not pasDig:
            window['-STATUS-DETALHADO-'].update("Nada alterado")
            continue
        if not os.path.exists(pasDig):
            window["-STATUS-DETALHADO-"].update("Caminho não existe!")
            continue
        if not os.path.isdir(pasDig):
            window["-STATUS-DETALHADO-"].update("Isso não é uma pasta")
            continue
        
        """ARMAZENA O FORMATO"""
        config['pasta_custom'] = pasDig

        if values['-FORMATO-APP-']:
            config['formato_selecionado'] = 'app'
        
        elif values['-FORMATO-TXT-']:
            config['formato_selecionado'] = 'txt'
        
        elif values['-FORMATO-MD-']:
            config['formato_selecionado'] = 'md'

        """ARMAZENA A PASTA CUSTOMIZADA"""
        config['modo_salva'] = 'custom'



        # Atualiza status
        status_msg = f"""
            📁 Pasta de Saída: {pasDig}

            📄 Formato: {config['formato_selecionado'].upper()}

            ⚡ Status: Pronto para gerar!"""
        
        window["-STATUS-DETALHADO-"].update(status_msg)
        sg.popup_quick_message(
            "Pasta confirmada!\n\nClique na aba 'Gerar' para continuar",
            auto_close_duration=1.6)
    
window.close()