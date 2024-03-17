from dataclasses import dataclass, field


@dataclass
class VQA:
    """
    Class to be filled for executing variational quantum algorithms through Qilimanjaro's QaaS.
    """

    vqa_dict: dict
    init_params: list
    optimizer_params: dict = None

    def __post_init__(self):
        if self.optimizer_params is None:
            self.optimizer_params = {}
