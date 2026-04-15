"""
Database models package.
Re-exports ORM classes for backward compatibility.
"""
from ..database import Base  # noqa: F401

# Auth
from .auth import User

# Records
from .records import AuditLog, ChatLog, HealthRecord

# Appointments
from .appointments import Appointment

# Clinical / Vitals
from .clinical import (
    CareEvent,
    ClinicalOrder,
    DiagnosticResult,
    MonitoringSignal,
    VitalObservation,
)

# Hospital
from .hospital import Admission, Bed, Department, Encounter, HospitalFacility

# Pharmacy
from .pharmacy import DispenseRecord, MedicationInventory, Prescription, PrescriptionItem

# Discharge
from .discharge import DischargeSummary

# Nursing
from .nursing import NursingTask

# Intelligence
from .intelligence import ClinicalAlert, PatientInsight

__all__ = [
    "Base",
    "User",
    "HealthRecord",
    "ChatLog",
    "AuditLog",
    "Appointment",
    "CareEvent",
    "ClinicalOrder",
    "DiagnosticResult",
    "MonitoringSignal",
    "VitalObservation",
    "HospitalFacility",
    "Department",
    "Bed",
    "Encounter",
    "Admission",
    "MedicationInventory",
    "Prescription",
    "PrescriptionItem",
    "DispenseRecord",
    "DischargeSummary",
    "NursingTask",
    "ClinicalAlert",
    "PatientInsight",
]
