import math
import random
from typing import Dict

import torch
import torch.nn as nn
import transformers

from models.logits_processors import ContrastiveLogitsProcessor
from trainers.base import BaseTrainer


class InversionTrainerNonAutoregressive(BaseTrainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ######################################################
        self.call_embedding_model = self.model.call_embedding_model

    def generate(self, inputs: Dict, generation_kwargs: Dict) -> torch.Tensor:
        return self.model.generate(
            inputs=inputs, generation_kwargs=generation_kwargs
        )

    def evaluation_loop(
        self, *args, **kwargs
    ) -> transformers.trainer_utils.EvalLoopOutput:
        """
        Run evaluation and returns metrics.

        Override to compute ppl from eval loss.
        """
        output = super().evaluation_loop(*args, **kwargs)

        metric_key_prefix = kwargs["metric_key_prefix"]
        try:
            perplexity = math.exp(output.metrics[f"{metric_key_prefix}_loss"])
        except OverflowError:
            perplexity = float("inf")
        output.metrics["eval_perplexity"] = perplexity

        return output
