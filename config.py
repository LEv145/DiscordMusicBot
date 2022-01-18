import toml


with open("config.toml") as fp:
    _config = toml.load(fp)

BOT_TOKEN = _config["bot"]["token"]
