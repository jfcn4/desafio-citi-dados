#ordem das camadas: bronze -> prata -> ouro

from src import exportar, ouro, prata

if __name__ == "__main__":
    prata.executar()          #bronze -> prata + log
    ouro.executar()           #prata  -> ouro + resposta
    exportar.executar()       #.xlsx com bronze, prata e log para o google sheets
