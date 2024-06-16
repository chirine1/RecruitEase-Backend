from uvicorn import run


from src.config.settings import Settings

def split_comma(x:str):
        return x.split(',')
   
def identity_func(x):
        return x

if __name__ == "__main__":
    
        run(
            "src.api:app",
            host="localhost",
            port=Settings().PORT,
            reload=True,
        )
