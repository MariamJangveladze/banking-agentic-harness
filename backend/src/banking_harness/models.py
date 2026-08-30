"""Typed contracts shared by the process graph, API and evaluations."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class RequestClass(StrEnum):
    NEW_IMPLEMENTATION = "NEW_IMPLEMENTATION"
    CHANGE_TO_EXISTING = "CHANGE_TO_EXISTING"


class SubjectType(StrEnum):
    PRODUCT = "PRODUCT"
    PROCESS = "PROCESS"
    PROCEDURE = "PROCEDURE"
    RULE = "RULE"


class CaseStatus(StrEnum):
    RUNNING = "running"
    NEEDS_INFORMATION = "needs_information"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    EVAL_ESCALATION = "eval_escalation"


class ChangeRequest(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    owner: str = Field(min_length=2, max_length=120)
    business_purpose: str = Field(min_length=10, max_length=4000)
    requested_change: str = Field(min_length=10, max_length=4000)
    subject_type: SubjectType = SubjectType.PROCESS
    existing_item_id: str | None = Field(default=None, max_length=120)
    risk_reference: str | None = Field(default=None, max_length=120)
    legal_reference: str | None = Field(default=None, max_length=120)
    infosec_reference: str | None = Field(default=None, max_length=120)
    aml_applicable: bool = False
    aml_reference: str | None = Field(default=None, max_length=120)
    related_department_reference: str | None = Field(default=None, max_length=120)


class Citation(BaseModel):
    source_id: str
    version: str
    excerpt: str


class ImpactFinding(BaseModel):
    domain: Literal["risk", "operations", "technology"]
    summary: str
    severity: Literal["low", "medium", "high"]
    citations: list[Citation]


class EvalResult(BaseModel):
    name: str
    score: float = Field(ge=0, le=1)
    threshold: float = Field(ge=0, le=1)
    passed: bool
    detail: str


class EvidenceEvent(BaseModel):
    event: str
    actor: str
    detail: str
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class HumanDecision(BaseModel):
    decision: Literal["approve", "reject"]
    reviewer: str = Field(min_length=2, max_length=120)
    comment: str = Field(default="", max_length=2000)
