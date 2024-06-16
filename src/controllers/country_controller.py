from typing import Annotated, Optional
from fastapi import  Depends
from src.models.country import Country as model
from src.schemas.country import CountryCreate as create_schema, CountryIn

from src.schemas.state import StateCreate
from src.services.country import CountryService
from src.services.state import StateService



class CountryController:

    def __init__(
        self,
        service: Annotated[CountryService, Depends()],
        state_service: Annotated[StateService, Depends()],
        
    ) -> None:
        self.service = service
        self.state_service = state_service
        
    async def create(self, body: create_schema):
        return await self.service.create(body)

    async def get_by_id(self, id:int):
        return await self.service.get_one(id)
    
    async def get_all(self):
        return await self.service.get_all()
    
    async def update(self, id:int, body: create_schema):
        return await self.service.update(id, body)

    async def delete(self, id:int):
        return await self.service.delete(id)
    
    async def init_countries(self):
        try:
            countries = ['USA', 'Canada', 'UK', 'Germany', 'India',
                        'Australia', 'Brazil', 'China', 'France', 'Italy', 
                        'Japan', 'Mexico', 'Russia', 'South Africa', 'South Korea',
                            'Spain', 'Sweden', 'Turkey', 'Argentina', 'Tunisia']
            country_states = {
            'USA': ['California', 'Texas', 'Florida', 'New York', 'Illinois', 'Pennsylvania', 'Ohio', 'Georgia'],
            'Canada': ['Ontario', 'Quebec', 'British Columbia', 'Alberta', 'Manitoba', 'Saskatchewan', 'Nova Scotia', 'New Brunswick'],
            'UK': ['England', 'Scotland', 'Wales', 'Northern Ireland', 'Greater London', 'West Midlands', 'Greater Manchester', 'West Yorkshire'],
            'Germany': ['Bavaria', 'Baden-Württemberg', 'North Rhine-Westphalia', 'Hesse', 'Saxony', 'Lower Saxony', 'Rhineland-Palatinate', 'Thuringia'],
            'India': ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh', 'Rajasthan', 'Gujarat', 'Kerala', 'West Bengal'],
            'Australia': ['New South Wales', 'Victoria', 'Queensland', 'Western Australia', 'South Australia', 'Tasmania', 'Northern Territory', 'Australian Capital Territory'],
            'Brazil': ['São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Bahia', 'Paraná', 'Rio Grande do Sul', 'Pernambuco', 'Ceará'],
            'China': ['Guangdong', 'Shandong', 'Henan', 'Sichuan', 'Jiangsu', 'Hebei', 'Hunan', 'Anhui'],
            'France': ['Île-de-France', 'Provence-Alpes-Côte d\'Azur', 'Auvergne-Rhône-Alpes', 'Nouvelle-Aquitaine', 'Occitanie', 'Hauts-de-France', 'Grand Est', 'Brittany'],
            'Italy': ['Lombardy', 'Lazio', 'Campania', 'Sicily', 'Veneto', 'Emilia-Romagna', 'Piedmont', 'Tuscany'],
            'Japan': ['Tokyo', 'Kanagawa', 'Osaka', 'Aichi', 'Hokkaido', 'Hyogo', 'Fukuoka', 'Saitama'],
            'Mexico': ['Jalisco', 'Mexico City', 'Nuevo León', 'Puebla', 'Guanajuato', 'Veracruz', 'Chihuahua', 'Coahuila'],
            'Russia': ['Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg', 'Nizhny Novgorod', 'Kazan', 'Chelyabinsk', 'Rostov-on-Don'],
            'South Africa': ['Gauteng', 'KwaZulu-Natal', 'Western Cape', 'Eastern Cape', 'Limpopo', 'Mpumalanga', 'North West', 'Free State'],
            'South Korea': ['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon', 'Gwangju', 'Ulsan', 'Suwon'],
            'Spain': ['Andalusia', 'Catalonia', 'Madrid', 'Valencia', 'Galicia', 'Castile and León', 'Basque Country', 'Canary Islands'],
            'Sweden': ['Stockholm', 'Västra Götaland', 'Skåne', 'Uppsala', 'Östergötland', 'Jönköping', 'Värmland', 'Dalarna'],
            'Turkey': ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya', 'Adana', 'Konya', 'Gaziantep'],
            'Argentina': ['Buenos Aires', 'Córdoba', 'Santa Fe', 'Mendoza', 'Tucumán', 'Entre Ríos', 'Salta', 'Misiones'],
            'Tunisia': ['Mahdia', 'Sfax', 'Sousse', 'Kairouan', 'Gabès', 'Bizerte', 'Aryanah', 'Tunis']
        }
            
            for country in countries:
                await self.service.create(create_schema(label=country))
            
            created_states = list()
            for country,states in country_states.items():
                for state in states :
                    created_states.append(await self.state_service.create(StateCreate(
                        label= state,
                        country=CountryIn(
                            label=country
                        )
                    )))
            return created_states
        except Exception as e: 
            print(e)