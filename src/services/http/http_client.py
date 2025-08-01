from src.services.http.dto.ibge_response_dto import Municipio
from config.envs import envsConfig
from typing import List
import requests

class HttpClient:
  def get(self, url: str):
    response = requests.get(url)
    if response.status_code == 200:
      data = response.json()
      return data
    return None

  def get_ibge_code_by_city_uf(self, city: str, uf: str):
    ibge_base_endpoint = envsConfig['IBGE_API']
    url = ibge_base_endpoint + f'/localidades/municipios/{city}'
    response = self.get(url)

    if response is None:
        return None

    municipios: List[Municipio] = [response] if isinstance(response, dict) else response
    for municipio in municipios:
        uf_municipio = municipio['microrregiao']['mesorregiao']['UF']['sigla']
        if uf_municipio.upper() == uf.upper():
            return municipio['id']
        
  def quotation(self, ibge_code: str, cost: float):
    #Monta o payload, apenas
     payload = {"ibge" : ibge_code, "custeio": cost}
     return payload
