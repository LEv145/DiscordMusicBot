import toml as _toml


with open("config.toml") as fp:
    _config = _toml.load(fp)

BOT_TOKEN = _config["bot"]["token"]
