import importlib
from typing import List, Optional, Union

import applications_superstaq
import cirq

import cirq_superstaq

try:
    import qtrl.sequencer
except ModuleNotFoundError:
    pass


class CompilerOutput:
    def __init__(
        self,
        circuits: Union[cirq.Circuit, List[cirq.Circuit]],
        seq: Optional["qtrl.sequencer.Sequence"] = None,
        jaqal_programs: List[str] = None,
        pulse_lists: Optional[Union[List[List], List[List[List]]]] = None,
    ) -> None:
        if isinstance(circuits, cirq.Circuit):
            self.circuit = circuits
            self.pulse_list = pulse_lists
        else:
            self.circuits = circuits
            self.pulse_lists = pulse_lists

        self.seq = seq
        self.jaqal_programs = jaqal_programs

    def has_multiple_circuits(self) -> bool:
        """Returns True if this object represents multiple circuits.

        If so, this object has .circuits and .pulse_lists attributes. Otherwise, this object
        represents a single circuit, and has .circuit and .pulse_list attributes.
        """
        return hasattr(self, "circuits")

    def __repr__(self) -> str:
        if not self.has_multiple_circuits():
            return (
                f"CompilerOutput({self.circuit!r}, {self.seq!r}, {self.jaqal_programs!r}, "
                f"{self.pulse_list!r})"
            )
        return (
            f"CompilerOutput({self.circuits!r}, {self.seq!r}, {self.jaqal_programs!r}, "
            f"{self.pulse_lists!r})"
        )


def read_json_aqt(json_dict: dict, circuits_list: bool) -> CompilerOutput:
    """Reads out returned JSON from SuperstaQ API's AQT compilation endpoint.

    Args:
        json_dict: a JSON dictionary matching the format returned by /aqt_compile endpoint
        circuits_list: bool flag that controls whether the returned object has a .circuits
            attribute (if True) or a .circuit attribute (False)
    Returns:
        a CompilerOutput object with the compiled circuit(s). If qtrl is available locally,
        the returned object also stores the pulse sequence in the .seq attribute and the
        list(s) of cycles in the .pulse_list(s) attribute.
    """
    seq = None
    pulse_lists = None

    if importlib.util.find_spec(
        "qtrl"
    ):  # pragma: no cover, b/c qtrl is not open source so it is not in cirq-superstaq reqs
        state = applications_superstaq.converters.deserialize(json_dict["state_jp"])

        seq = qtrl.sequencer.Sequence(n_elements=1)
        seq.__setstate__(state)
        seq.compile()

        pulse_lists = applications_superstaq.converters.deserialize(json_dict["pulse_lists_jp"])

    compiled_circuits = cirq_superstaq.serialization.deserialize_circuits(
        json_dict["cirq_circuits"]
    )
    if circuits_list:
        return CompilerOutput(circuits=compiled_circuits, seq=seq, pulse_lists=pulse_lists)

    pulse_list = pulse_lists[0] if pulse_lists is not None else None
    return CompilerOutput(circuits=compiled_circuits[0], seq=seq, pulse_lists=pulse_list)


def read_json_qscout(json_dict: dict, circuits_list: bool) -> CompilerOutput:
    """Reads out returned JSON from SuperstaQ API's QSCOUT compilation endpoint.

    Args:
        json_dict: a JSON dictionary matching the format returned by /qscout_compile endpoint
        circuits_list: bool flag that controls whether the returned object has a .circuits
            attribute (if True) or a .circuit attribute (False)
    Returns:
        a CompilerOutput object with the compiled circuit(s) and a list jaqal programs
        represented as strings
    """

    compiled_circuits = cirq_superstaq.serialization.deserialize_circuits(
        json_dict["cirq_circuits"]
    )

    if circuits_list:
        return CompilerOutput(
            circuits=compiled_circuits, jaqal_programs=json_dict["jaqal_programs"]
        )

    return CompilerOutput(
        circuits=compiled_circuits[0], jaqal_programs=json_dict["jaqal_programs"][0]
    )
