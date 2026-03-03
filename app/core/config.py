from pydantic_settings import BaseSettings

class Settings(BaseSettings):

	app_name: str = "cell-api"
	debug: bool = True
	database_url: str = "sqlite+aiosqlite:///./cell.db"

	class Config:
		env_file = ".env"

settings = Settings()