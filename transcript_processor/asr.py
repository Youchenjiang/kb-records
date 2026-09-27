#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Safe ASR & Hardware Guardrail Module
Provides VRAM-constrained GPU inference settings, periodic garbage collection,
and boundary-aware audio chunk interval computation.
"""

from typing import Dict, List, Optional, Tuple, Union
import gc
import os


class SafeASREngine:
    """
    Manages safe execution of local ASR models with hardware constraints
    to prevent out-of-memory errors and display driver TDR resets.
    """

    def __init__(
        self,
        max_vram_fraction: float = 0.60,
        chunk_duration_sec: float = 45.0,
        overlap_sec: float = 1.5,
        device: Optional[str] = None,
    ):
        self.max_vram_fraction = min(max(max_vram_fraction, 0.1), 0.9)
        self.chunk_duration_sec = max(chunk_duration_sec, 5.0)
        self.overlap_sec = max(overlap_sec, 0.0)
        self.device = device or self._detect_device()

        self._configure_gpu_guardrails()

    def _detect_device(self) -> str:
        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
        except ImportError:
            pass
        return "cpu"

    def _configure_gpu_guardrails(self):
        """
        Enforce memory fraction limit on CUDA to safeguard OS and remote sessions.
        """
        if self.device == "cuda":
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.set_per_process_memory_fraction(self.max_vram_fraction)
            except (ImportError, RuntimeError):
                pass

    def cleanup_memory(self):
        """
        Perform aggressive garbage collection and empty CUDA cache.
        """
        gc.collect()
        if self.device == "cuda":
            try:
                import torch
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except (ImportError, RuntimeError):
                pass

    def get_vram_info(self) -> Dict[str, Union[float, str]]:
        """
        Return current GPU memory usage and configuration stats.
        """
        info: Dict[str, Union[float, str]] = {
            "device": self.device,
            "max_fraction": self.max_vram_fraction,
        }
        if self.device == "cuda":
            try:
                import torch
                if torch.cuda.is_available():
                    allocated_bytes = torch.cuda.memory_allocated()
                    reserved_bytes = torch.cuda.memory_reserved()
                    info["allocated_mb"] = round(allocated_bytes / (1024 * 1024), 2)
                    info["reserved_mb"] = round(reserved_bytes / (1024 * 1024), 2)
                    info["device_name"] = torch.cuda.get_device_name(0)
            except (ImportError, RuntimeError):
                pass
        return info

    def compute_chunk_intervals(
        self,
        total_duration_sec: float,
        chunk_duration: Optional[float] = None,
        overlap: Optional[float] = None,
    ) -> List[Tuple[float, float]]:
        """
        Calculate overlapping time intervals for safe sliding-window transcription.
        """
        dur = chunk_duration or self.chunk_duration_sec
        ovlp = overlap if overlap is not None else self.overlap_sec

        if total_duration_sec <= dur:
            return [(0.0, total_duration_sec)]

        step = max(dur - ovlp, 1.0)
        intervals: List[Tuple[float, float]] = []
        current_start = 0.0

        while current_start < total_duration_sec:
            current_end = min(current_start + dur, total_duration_sec)
            intervals.append((round(current_start, 2), round(current_end, 2)))
            if current_end >= total_duration_sec:
                break
            current_start += step

        return intervals
