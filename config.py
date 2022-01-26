import toml as _toml


with open("config.toml") as fp:
    _config = _toml.load(fp)

BOT_TOKEN: str = _config["bot"]["token"]
DATABASE_URL: str = _config["database"]["url"]
