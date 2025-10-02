import json
import os
from typing import Optional, Dict, Any, List

CLIENTES_FILE = "clientes.json"
PROFISSIONAIS_FILE = "profissionais.json"

def _load_json(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _save_json(path: str, data: List[Dict[str, Any]]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def cliente_listar_raw() -> List[Dict[str,Any]]:
    return _load_json(CLIENTES_FILE)

def cliente_listar_objs() -> List[Dict[str,Any]]:
    """Retorna lista de clientes (dicionários). Garante que o campo 'senha' exista."""
    lista = cliente_listar_raw()
    for c in lista:
        if "senha" not in c:
            c["senha"] = ""
    return lista

def cliente_listar_id_raw(id: int) -> Optional[Dict[str,Any]]:
    for c in cliente_listar_objs():
        if c.get("id") == id:
            return c
    return None

def cliente_inserir_raw(nome: str, email: str, fone: str, senha: str):
    lista = cliente_listar_raw()
    next_id = 1
    if lista:
        next_id = max([c.get("id",0) for c in lista]) + 1
    novo = {"id": next_id, "nome": nome, "email": email, "fone": fone, "senha": senha}
    lista.append(novo)
    _save_json(CLIENTES_FILE, lista)
    return novo

def cliente_atualizar_raw(id: int, nome: str, email: str, fone: str, senha: str) -> bool:
    lista = cliente_listar_raw()
    changed = False
    for i,c in enumerate(lista):
        if c.get("id") == id:
            lista[i]["nome"] = nome
            lista[i]["email"] = email
            lista[i]["fone"] = fone
            lista[i]["senha"] = senha
            changed = True
            break
    if changed:
        _save_json(CLIENTES_FILE, lista)
    return changed

def cliente_excluir_raw(id: int) -> bool:
    lista = cliente_listar_raw()
    nova = [c for c in lista if c.get("id") != id]
    if len(nova) != len(lista):
        _save_json(CLIENTES_FILE, nova)
        return True
    return False

def cliente_criar_admin():
    """Garante que exista um cliente com email 'admin' e senha '1234'."""
    lista = cliente_listar_raw()
    for c in lista:
        if c.get("email") == "admin":

            if c.get("senha","") == "":
                c["senha"] = "1234"
                _save_json(CLIENTES_FILE, lista)
            return
    # criar admin
    novo = {"id": (max([x.get("id",0) for x in lista]) + 1) if lista else 1,
           "nome": "admin", "email": "admin", "fone": "fone", "senha": "1234"}
    lista.append(novo)
    _save_json(CLIENTES_FILE, lista)

def cliente_autenticar(email: str, senha: str) -> Optional[Dict[str,Any]]:
    for c in cliente_listar_objs():
        if c.get("email") == email and c.get("senha") == senha:
            return {"id": c.get("id"), "nome": c.get("nome")}
    return None


def profissional_listar_raw() -> List[Dict[str,Any]]:
    return _load_json(PROFISSIONAIS_FILE)

def profissional_listar_objs() -> List[Dict[str,Any]]:
    lista = profissional_listar_raw()
    for p in lista:
        if "email" not in p:
            p["email"] = ""
        if "senha" not in p:
            p["senha"] = ""
    return lista

def profissional_inserir_raw(nome: str, profissao: str, email: str = "", senha: str = ""):
    lista = profissional_listar_raw()
    next_id = 1
    if lista:
        next_id = max([p.get("id",0) for p in lista]) + 1
    novo = {"id": next_id, "nome": nome, "profissao": profissao, "email": email, "senha": senha}
    lista.append(novo)
    _save_json(PROFISSIONAIS_FILE, lista)
    return novo

def profissional_atualizar_raw(id: int, nome: str, profissao: str, email: str, senha: str) -> bool:
    lista = profissional_listar_raw()
    changed = False
    for i,p in enumerate(lista):
        if p.get("id") == id:
            lista[i]["nome"] = nome
            lista[i]["profissao"] = profissao
            lista[i]["email"] = email
            lista[i]["senha"] = senha
            changed = True
            break
    if changed:
        _save_json(PROFISSIONAIS_FILE, lista)
    return changed

def profissional_excluir_raw(id: int) -> bool:
    lista = profissional_listar_raw()
    nova = [p for p in lista if p.get("id") != id]
    if len(nova) != len(lista):
        _save_json(PROFISSIONAIS_FILE, nova)
        return True
    return False

def profissional_autenticar(email: str, senha: str) -> Optional[Dict[str,Any]]:
    for p in profissional_listar_objs():
        if p.get("email") == email and p.get("senha") == senha:
            return {"id": p.get("id"), "nome": p.get("nome")}
    return None
