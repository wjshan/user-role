import os

from dynaconf import Dynaconf

HERE = os.path.dirname(os.path.abspath(__file__))

settings = Dynaconf(
    envvar_prefix="user_role",
    preload=[".env", os.path.join(HERE, "default.toml")],
    settings_files=["settings.toml"],
    environments=True,
    env_switcher="user_role_env",
    load_dotenv=True,
    merge_enabled=True
)
"""
# How to use this application settings

```
from user_role.config import settings
```

## Acessing variables

```
settings.get("SECRET_KEY", default="sdnfjbnfsdf")
settings["SECRET_KEY"]
settings.SECRET_KEY
settings.db.uri
settings["db"]["uri"]
settings["db.uri"]
settings.DB__uri
```

## Modifying variables

### On files

settings.toml
```
[development]
KEY=value
```

### As environment variables
```
export user_role_KEY=value
export user_role_KEY="@int 42"
export user_role_KEY="@jinja {{ this.db.uri }}"
export user_role_DB__uri="@jinja {{ this.db.uri | replace('db', 'data') }}"
```

### Switching environments
```
user_role_ENV=production user_role run
```

Read more on https://dynaconf.com
"""
