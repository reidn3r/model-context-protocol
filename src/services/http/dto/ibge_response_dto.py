from typing import TypedDict, Union, List

class Regiao(TypedDict):
    id: int
    sigla: str
    nome: str

class UF(TypedDict):
    id: int
    sigla: str
    nome: str
    regiao: Regiao

class Mesorregiao(TypedDict):
    id: int
    nome: str
    UF: UF

class Microrregiao(TypedDict):
    id: int
    nome: str
    mesorregiao: Mesorregiao

class RegiaoIntermediaria(TypedDict):
    id: int
    nome: str
    UF: UF

class RegiaoImediata(TypedDict):
    id: int
    nome: str
    regiao_intermediaria: RegiaoIntermediaria

class Municipio(TypedDict):
    id: int
    nome: str
    microrregiao: Microrregiao
    regiao_imediata: RegiaoImediata

# Tipo que representa a resposta da API, que pode ser um único município ou uma lista de municípios
IbgeResponse = Union[Municipio, List[Municipio]]