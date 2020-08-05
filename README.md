# notificacoesAcoes

Notificações de Ações

Criado por: Bruno Ferreira
Versão: 1.3.2

App com GUI baseada em Tkinter que permite enviar notificações para o Desktop e Email quando uma certa Ação/Índice sai de um intervalo de valor definido na interface.
Permite verificar repetidamente.

Notas:
Para usar as notificações por mail é necessário preencher os dados (EMAIL e PASSWORD) dentro do script. A conta escolhida tem de ter a opção "Acesso a apps menos seguras" ativada para ser possível utilizá-la para o envio de mails.

Required libs:
- tkinter
- yahoo_fin
- yfinance
- plyer
- smtplib

Known bugs:
- Não verifica se o email está na forma correta
- Outras verificações de inputs
