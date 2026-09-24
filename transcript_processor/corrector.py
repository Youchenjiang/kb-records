#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Domain Vocabulary & ASR Error Correction Module
Provides extensible domain-specific dictionaries and replacement engines.
"""

from typing import Dict, List, Optional, Tuple, Union
import json
from pathlib import Path


DomainDict = List[Tuple[str, str]]


COMMON_ASR_ERRORS: DomainDict = [
    ("來入不明", "來路不明"),
    ("來顧名", "來路不明"),
    ("服務正業", "不務正業"),
    ("市機上面", "實機上面"),
    ("城市碼", "程式碼"),
    ("城 市 碼", "程式碼"),
    ("精靈演說", "精彩演說"),
    ("指系統", "子系統"),
    ("指 系統", "子系統"),
    ("無克蘭", "烏克蘭"),
    ("最超", "最操"),
    ("很超", "很操"),
    ("一康", "HITCON"),
    ("PTB", "PCB"),
    ("漢街", "焊接"),
]

HITCON_SECURITY_TERMS: DomainDict = [
    # Kernel & Mobile Exploit
    ("M GPQ driver", "Mali GPU driver"),
    ("Mali driver", "Mali driver"),
    ("CONFIG_MALI_BIFROST_NO_MALI", "CONFIG_MALI_BIFROST_NO_MALI"),
    ("CD20256349", "CVE-2025-6349"),
    ("C20258045", "CVE-2025-8045"),
    ("kprobe 是", "kprobes 是"),
    ("KP,", "kprobes，"),
    ("CI header", "CFI header"),
    ("CI,", "CFI，"),
    ("CI ", "CFI "),
    ("dble free", "Double Free"),
    ("dble", "Double Free"),
    ("大國網", "大掌櫃"),
    ("swaper pgdp", "swapper_pg_dir"),
    # ADB & POS Terminal
    ("磨改了 B", "魔改了 adbd"),
    ("XCB", "xcbd"),
    ("IS2048", "RSA-2048"),
    ("CW159", "Zip-Slip 任意檔案覆寫漏洞"),
    ("bzvbx", "BusyBox"),
    ("小龍蝦", "OpenClaw"),
    # Supply Chain
    ("哈尼帕", "Honeypot（蜜罐）"),
    ("Ract to SH", "React-to-Shell"),
    ("execution context keying", "Execution Context Keying"),
    ("sitecustomize.py", "sitecustomize.py"),
]

MICROSOFT_CLOUD_AI_TERMS: DomainDict = [
    # Evaluation & Red Teaming
    ("AI rating", "AI Red Teaming"),
    ("p 專叫 p", "專案叫 PyRIT"),
    ("PyRIT", "PyRIT"),
    ("sag control specification", "SAG Control Specification"),
    ("sag control", "SAG Control"),
    ("UL315", "UL 315"),
    ("Clear VIA AI", "Clearview AI"),
    # DevSecOps & GHAS
    ("GHS", "GHAS"),
    ("DHUB", "GitHub"),
    ("admin security", "Advanced Security"),
    ("dpend cloud", "Defender for Cloud"),
    ("dependable cloud", "Defender for Cloud"),
    ("dependable", "Defender"),
    ("c security", "Code Security"),
    ("sakeup", "SecOps"),
    ("sup 這個團隊", "SecOps 這個團隊"),
    ("Sup 呢", "SecOps 呢"),
    ("MAGENTA", "MAGENTA"),
    ("M das", "MAGENTA"),
    # Tokenomics & Foundry
    ("tokconomics", "Tokenomics"),
    ("tokconomic", "Tokenomics"),
    ("M65 profiler", "M365 Profiler"),
    ("M365 profile", "M365 Profiler"),
    ("54", "Phi-4"),
    ("5 4", "Phi-4"),
    ("foundary", "Foundry"),
    ("agent faces", "Agent Traces"),
    ("spent tele", "Spend Telemetry"),
    ("spent element", "Spend Telemetry"),
    # Agentic SOC & Security Copilot
    ("centel", "Sentinel"),
    ("poject position", "Project Perception"),
    ("project perception", "Project Perception"),
    ("perception", "Perception"),
    ("sec compiler", "Security Copilot"),
    ("SQuriler", "Security Copilot"),
    ("se compiler", "Security Copilot"),
    ("KQL", "KQL"),
    ("hunting 的 ent", "Threat Hunting Agent"),
    ("cft", "Conflict"),
    ("Zav", "Zav Webshop"),
]


class CorrectionEngine:
    """
    Manages domain-specific vocabulary and ASR error corrections.
    """

    def __init__(self):
        self.domains: Dict[str, DomainDict] = {
            "common": list(COMMON_ASR_ERRORS),
            "hitcon": list(HITCON_SECURITY_TERMS),
            "microsoft": list(MICROSOFT_CLOUD_AI_TERMS),
        }

    def register_rule(self, domain: str, error_term: str, target_term: str):
        if domain not in self.domains:
            self.domains[domain] = []
        self.domains[domain].append((error_term, target_term))

    def register_rules(self, domain: str, rules: DomainDict):
        if domain not in self.domains:
            self.domains[domain] = []
        self.domains[domain].extend(rules)

    def load_from_json(self, path: Union[str, Path], domain: str = "custom"):
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Dictionary file not found: {path}")
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            # data can be list of [old, new] or dict {old: new}
            if isinstance(data, dict):
                rules = list(data.items())
            elif isinstance(data, list):
                rules = [(item[0], item[1]) for item in data]
            else:
                raise ValueError("JSON must be a list of pairs or an object.")
            self.register_rules(domain, rules)

    def correct(self, text: str, domains: Optional[List[str]] = None) -> str:
        """
        Apply registered replacement rules in selected domains (defaults to all).
        """
        active_domains = domains if domains is not None else list(self.domains.keys())
        for d in active_domains:
            if d in self.domains:
                for old_val, new_val in self.domains[d]:
                    text = text.replace(old_val, new_val)
        return text
