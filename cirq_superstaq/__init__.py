# Copyright 2021 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cirq_superstaq import serialization
from cirq_superstaq._init_vars import API_URL, API_VERSION
from cirq_superstaq.custom_gates import (
    AceCR,
    AceCRMinusPlus,
    AceCRMinusPlusXNeg90Target,
    AceCRPlusMinus,
    AceCRPlusMinusXNeg90Target,
    Barrier,
    CR,
    FermionicSWAPGate,
    ParallelGates,
    ZX,
    ZXPowGate,
)
from cirq_superstaq.job import Job
from cirq_superstaq.service import Service
from cirq_superstaq.superstaq_exceptions import (
    SuperstaQException,
    SuperstaQModuleNotFoundException,
    SuperstaQNotFoundException,
    SuperstaQUnsuccessfulJobException,
)

__all__ = [
    "AceCR",
    "AceCRMinusPlus",
    "AceCRMinusPlusXNeg90Target",
    "AceCRPlusMinus",
    "AceCRPlusMinusXNeg90Target",
    "API_URL",
    "API_VERSION",
    "Barrier",
    "CR",
    "FermionicSWAPGate",
    "Job",
    "ParallelGates",
    "serialization",
    "Service",
    "SuperstaQException",
    "SuperstaQModuleNotFoundException",
    "SuperstaQNotFoundException",
    "SuperstaQUnsuccessfulJobException",
    "ZX",
    "ZXPowGate",
]
