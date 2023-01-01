import os
from pathlib import Path
from typing import List

import yaml
from pydantic import BaseModel

config_file = os.path.dirname(__file__) + "/local/config.yaml"


class General(BaseModel):
    site_cache: str
    period: int


class FlatParams(BaseModel):
    area_min: int
    rooms_min: int
    rooms_max: int
    rent_base_max: int
    rent_total_max: int
    wbs: int


class Filter(BaseModel):
    allow: dict
    block: dict


class Search(BaseModel):
    sites: List[str]
    flat_params: FlatParams
    filter: Filter


class Telegram(BaseModel):
    name: str
    max_field_len: int
    api_key: str
    ids: List[int]


class Maps(BaseModel):
    center: str
    group_size: int
    key: str
    zoom: int


class Model(BaseModel):
    general: General
    search: Search
    telegram: Telegram
    maps: Maps


with open(config_file, "r") as file:
    config_raw = yaml.safe_load(file)

general = General.parse_obj(config_raw["general"])
search = Search.parse_obj(config_raw["search"])
telegram = Telegram.parse_obj(config_raw["telegram"])
maps = Maps.parse_obj(config_raw["maps"])

cache_folder = Path(general.site_cache)
cache_folder.mkdir(exist_ok=True)
