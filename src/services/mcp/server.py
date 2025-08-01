from src.registry.registry import mcp
from src.services.http.dto.ibge_response_dto import Municipio
from src.main import container
from typing import Annotated
from pydantic import Field
import math

@mcp.tool(description="""Calcula área do quadrado dado o lado.""")
def area_square(
    side: Annotated[float, Field(description="Comprimento do lado do quadrado em unidades de medida")]
) -> float:
    return side * side

@mcp.tool(description="""Calcula área do círculo dado o raio.""")
def area_circle(
    radius: Annotated[float, Field(description="Raio do círculo em unidades de medida")]
) -> float:
    return math.pi * radius * radius

@mcp.tool(description=
    '''
        Encontra o código IBGE de um municipio por meio de uma chamada REST 
        para a API do ibge informando o nome do município.
    '''
    )
def get_ibge_code(
    city: Annotated[str, Field(description="Nome da cidade (OBRIGATÓRIO)")],
    uf: Annotated[str, Field(description="Sigla do estado (OBRIGATÓRIO)")]
) -> Municipio:
    http_client = container.http_client()
    return http_client.get_ibge_code_by_city_uf(city, uf)

@mcp.tool(description=
    '''
        Realiza cotacao baseado em dados como cidade, 
        estado (sigla), area e custeio ou lmi.
        LMI e Custeio são opcionais, de forma que apenas um deles deve ser informado.
    ''',
    )
async def compute_cotacao(
    city: Annotated[str, Field(description="Nome da cidade (OBRIGATÓRIO)")],
    uf: Annotated[str, Field(description="Sigla do Estado (OBRIGATÓRIO)")], 
    custeio: Annotated[float | None, Field(description="Valor de Custeio (OPCIONAL)")],
    lmi: Annotated[float | None, Field(description="Valor de Limite Máximo de Indenização (OPCIONAL)")],
    area: Annotated[float, Field(description="Area total Segurada (OBRIGATÓRIO)")],
    unidade_area: Annotated[str, Field(description='''
        Unidade de Medida da área informada. Deve ser formatado para m2 (metros quadrados) ou ha (hectares). 
        Caso não seja informado em nenhuma das medidas, retorne mensagem de erro 
        especificando as unidades aceitáveis'''
        )],
    ):
    http_client = container.http_client()

    #Normaliza a cidade: remove acentos e converte para lowercase
    city = ''.join(char for char in city.lower() if char.isalnum())

    ibge_code: Municipio = http_client.get_ibge_code_by_city_uf(city, uf)
    final_cost = lmi
    if unidade_area == 'm2':
        area = area*0.0001

    if custeio and not lmi:
        final_cost = area * custeio

    return http_client.quotation(ibge_code, final_cost)

@mcp.tool(description=
    '''
    Informa aos usuário os parametros faltantes 
    para a chamada de uma determinada função
    '''
    )
def discover(message: str) -> str:
    return message

if __name__ == "__main__":
    mcp.run()