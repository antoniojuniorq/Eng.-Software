import json
from datetime import date, datetime
from abc import ABC, abstractmethod
from typing import List, Dict
import os


class Visita:
    META_DIARIA = 25

    def __init__(self, agente_nome, bairro, endereco, status_casa, qtd_criadouros, area_risco, hora_entrada, tempo_visita, observacoes="",):
        self.data_visita = date.today()
        self.hora_entrada = hora_entrada
        self.tempo_visita = tempo_visita
        self.agente_nome = agente_nome
        self.bairro = bairro
        self.endereco = endereco
        self.status_casa = status_casa
        self.qtd_criadouros = qtd_criadouros
        self.area_risco = area_risco
        self.observacoes = observacoes

    def to_dict(self):
        return {
            "data_visita": self.data_visita.isoformat(),
            "hora_entrada": self.hora_entrada.strftime("%H:%M"),
            "tempo_visita": self.tempo_visita,
            "agente_nome": self.agente_nome,
            "bairro": self.bairro,
            "endereco": self.endereco,
            "status_casa": self.status_casa,
            "qtd_criadouros": self.qtd_criadouros,
            "area_risco": self.area_risco,
            "observacoes": self.observacoes,
        }

    @staticmethod
    def from_dict(d):
        return Visita(
            agente_nome=d["agente_nome"],
            bairro=d["bairro"],
            endereco=d["endereco"],
            status_casa=d["status_casa"],
            qtd_criadouros=d["qtd_criadouros"],
            area_risco=d["area_risco"],
            hora_entrada=datetime.strptime(d["hora_entrada"], "%H:%M"),
            tempo_visita=d["tempo_visita"],
            observacoes=d.get("observacoes", ""),
        )

    def __str__(self):
        return (
            f"[{self.data_visita}] {self.agente_nome} - {self.bairro}, {self.endereco} "
            f"({self.status_casa}) | Criadouros: {self.qtd_criadouros} | "
            f"Risco: {'Sim' if self.area_risco else 'NC#o'} | "
            f"Inicío: {self.hora_entrada.strftime('%H:%M')} | "
            f"Duração: {self.tempo_visita} min"
        )


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class RegistrarVisitaCommand(Command):
    def __init__(self, visitas: List[Visita], agente_nome, arquivo_json):
        self.visitas = visitas
        self.agente_nome = agente_nome
        self.arquivo_json = arquivo_json

    def execute(self):
        print("\n Nova Visita ")
        bairro = input("Bairro: ")
        endereco = input("Endereço: ")

        print("Status da casa:")
        print("[1] Visitada")
        print("[2] Fechada")
        opc = input("Escolha: ")

        hora_entrada = datetime.now()
        criadouros = 0
        risco = False
        obs = ""
        tempo = 0

        if opc == "1":
            status = "Visitada"

            hora_str = input("Horário de entrada (HH:MM): ")
            try:
                hora_entrada = datetime.strptime(hora_str, "%H:%M")
            except ValueError:
                print("Horário inválido! Usando o horário atual.")
                hora_entrada = datetime.now()

            tem_foco = input("A casa tinha foco de dengue? (s/n): ").lower() == "s"
            if tem_foco:
                status = "Com foco"

            criadouros = int(input("Qtd de criadouros encontrados: "))
            risco = input("Área de risco? (s/n): ").lower() == "s"
            obs = input("Observações: ")

            tempo = int(input("Tempo de visita (minutos): "))

        elif opc == "2":
            status = "Fechada"

        else:
            print("Opção inválida! Considerando como Visitada.")
            status = "Visitada"

        visita = Visita(
            self.agente_nome, bairro, endereco, status, criadouros, risco, hora_entrada, tempo, obs,)

        self.visitas.append(visita)
        self.salvar_json()
        print("\nRegistrado e salvo com sucesso!")

    def salvar_json(self):
        dados = [v.to_dict() for v in self.visitas]
        with open(self.arquivo_json, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)


class GerarRelatorioCommand(Command):
    def __init__(self, visitas: List[Visita]):
        self.visitas = visitas

    def execute(self):
        print("\n=> Relatório de Visitas")
        total = sum(v.status_casa.lower() in ["visitada", "com foco"] for v in self.visitas)
        fechadas = sum(v.status_casa.lower() == "fechada" for v in self.visitas)
        focos = sum(v.status_casa.lower() == "com foco" for v in self.visitas)
        risco = sum(v.area_risco for v in self.visitas)
        tempo_total = sum(v.tempo_visita for v in self.visitas)
        media_tempo = tempo_total / total if total > 0 else 0

        for v in self.visitas:
            print(v)

        print("\n=> Resumo")
        print(f"Casas registradas: {len(self.visitas)}")
        print(f"Casas visitadas (para meta): {total}")
        print(f"Fechadas: {fechadas}")
        print(f"Com foco: {focos}")
        print(f"Áreas de risco: {risco}")
        print(f"Tempo total em campo: {tempo_total} min")
        print(f"Tempo médio por casa: {media_tempo:.1f} min")

        meta = Visita.META_DIARIA
        progresso = (total / meta) * 100 if meta > 0 else 0
        print(f"Progresso da meta: {total}/{meta} casas ({progresso:.1f}%)")

        if total >= meta:
            print("Meta diária alcançada! Parabéns!")
        else:
            print(f"Faltam {meta - total} casas para atingir a meta.")

class CommandExecutor:
    def execute_command(self, command: Command):
        command.execute()
        
class LoginManager:
    def __init__(self, arquivo_agentes="agentes.json"):
        self.arquivo_agentes = arquivo_agentes
        self.agentes = self.carregar_agentes()

    def carregar_agentes(self) -> Dict[str, str]:
        if not os.path.exists(self.arquivo_agentes):
            return {}
        with open(self.arquivo_agentes, "r", encoding="utf-8") as f:
            return json.load(f)

    def salvar_agentes(self):
        with open(self.arquivo_agentes, "w", encoding="utf-8") as f:
            json.dump(self.agentes, f, indent=4, ensure_ascii=False)

    def registrar_agente(self):
        print("\n=> Novo Agente")
        nome = input("Nome do agente: ").strip()
        senha = input("Defina uma senha: ").strip()
        self.agentes[nome] = senha
        self.salvar_agentes()
        print(f"Agente '{nome}' registrado com sucesso!")

    def login(self) -> str:
        print("\n=> Login de Agente")
        nome = input("Nome: ").strip()
        senha = input("Senha: ").strip()

        if nome in self.agentes and self.agentes[nome] == senha:
            print(f"Login bem-sucedido! Bem-vindo(a), {nome}.")
            return nome
        else:
            print("Usuário ou senha incorretos.")
            return None

class ACEMapApp:
    def __init__(self):
        self.executor = CommandExecutor()
        self.login_manager = LoginManager()
        self.visitas = []
        self.arquivo_json = "visitas.json"
        self.carregar_visitas()

    def carregar_visitas(self):
        if os.path.exists(self.arquivo_json):
            with open(self.arquivo_json, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.visitas = [Visita.from_dict(v) for v in dados]

    def iniciar(self):
        print("=== ACE-MAP - Sistema do Agente de Endemias ===")

        while True:
            print("\n[1] Login")
            print("[2] Registrar novo agente")
            print("[0] Sair")
            op = input("Escolha: ")

            if op == "1":
                agente = self.login_manager.login()
                if agente:
                    self.menu_agente(agente)
            elif op == "2":
                self.login_manager.registrar_agente()
            elif op == "0":
                print("\nEncerrando ACE-MAP. AtC) logo!")
                break
            else:
                print("Opção inválida.")

    def menu_agente(self, agente):
        while True:
            print(f"\n=> Menu do Agente: {agente}")
            print("[1] Registrar visita")
            print("[2] Gerar relatório")
            print("[0] Logout")
            op = input("Escolha: ")

            if op == "1":
                cmd = RegistrarVisitaCommand(self.visitas, agente, self.arquivo_json)
                self.executor.execute_command(cmd)
            elif op == "2":
                cmd = GerarRelatorioCommand(self.visitas)
                self.executor.execute_command(cmd)
            elif op == "0":
                print("Logout realizado.")
                break
            else:
                print("Opção inválida.")


if __name__ == "__main__":
    app = ACEMapApp()
    app.iniciar()
