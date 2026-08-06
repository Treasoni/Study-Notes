"""实体名解析：entity_map.yaml + rapidfuzz 模糊匹配。

resolve() 输入「entity_id 或用户口吻的名称/别名」，返回规范 entity_id；
匹配不上返回 None，由调用方（main.py）组织面向用户的错误提示。
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml
from rapidfuzz import fuzz, process

ENTITY_ID_RE = re.compile(r"^[a-z][a-z0-9_]*\.[a-z0-9_]+$")


class EntityResolver:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.entities: list[dict] = []
        self._by_id: dict[str, dict] = {}   # entity_id -> entity
        self._label_to_id: dict[str, str] = {}  # name/alias -> entity_id
        self._load()

    def _load(self) -> None:
        data = yaml.safe_load(self.path.read_text(encoding="utf-8")) or {}
        self.entities = data.get("entities", [])
        for ent in self.entities:
            eid = ent.get("entity_id")
            if not eid:
                continue
            self._by_id[eid] = ent
            labels = [ent.get("name")] + list(ent.get("aliases", []) or [])
            for label in labels:
                if label:
                    self._label_to_id[str(label).strip().lower()] = eid

    def is_valid_entity_id(self, text: str) -> bool:
        """判断一段文本是否本身就是合法的 HA entity_id。"""
        return bool(ENTITY_ID_RE.match(text))

    def has_entity_id(self, text: str) -> bool:
        """entity_id 是否已存在于映射表（大小写不敏感）。"""
        return text in self._by_id

    def resolve(self, text: str | None) -> str | None:
        """返回规范 entity_id；解析失败返回 None。"""
        raw = (text or "").strip()
        if not raw:
            return None

        # 1) 直接命中 entity_id
        if raw in self._by_id:
            return raw

        # 2) 精确命中 name/alias（大小写不敏感）
        key = raw.lower()
        if key in self._label_to_id:
            return self._label_to_id[key]

        # 3) 看起来像 entity_id 但不在映射表 -> 不再模糊（避免把乱串当实体）
        if self.is_valid_entity_id(raw):
            return None

        # 4) 模糊匹配名称/别名（WRatio，阈值 80）。
        #    用 label 列表 + 显式查表，避免不同 rapidfuzz 版本对 dict choices 返回结构不一致。
        if not self._label_to_id:
            return None
        labels = list(self._label_to_id.keys())
        best = process.extractOne(raw, labels, scorer=fuzz.WRatio, score_cutoff=80)
        if best is None:
            return None
        return self._label_to_id[best[0]]

    def list_entities(self) -> list[str]:
        """向 LLM 暴露的可用实体清单（便于提示词注入）。"""
        return sorted(self._by_id.keys())
