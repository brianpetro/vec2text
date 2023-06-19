from datetime import datetime

from slurmpy import Slurm


all_beir_datasets = [
    ####### public datasets #######
    "arguana",
    "climate-fever",
    "cqadupstack",
    "dbpedia-entity",
    "fever",
    "fiqa",
    "hotpotqa",
    "msmarco",
    "nfcorpus",
    "nq",
    "quora",
    "scidocs",
    "scifact",
    "trec-covid",
    "webis-touche2020",
    ####### private datasets #######
    "signal1m",
    "trec-news",
    "robust04",
    "bioasq",
]

base_command = """
python evaluate_models.py {alias} \
--num_samples 500 \
--return_best_hypothesis {return_best_hypothesis} \
--num_gen_recursive_steps {num_gen_recursive_steps} \
--sequence_beam_width {sequence_beam_width} \
--beam_width {beam_width} \
--dataset {dataset}
"""

ACTUALLY_RUN_COMMAND = True


def run_command(cmd: str, job_desc: str):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    job_name = f"{dt_string} {job_desc}"
    ##
    print("job_name >>", job_name)
    print("cmd >>", cmd.strip())
    ##

    if ACTUALLY_RUN_COMMAND:
        slurm = Slurm(
            job_name,
            slurm_kwargs={
                "partition": "gpu", # rush,gpu
                "gres": "gpu:1",
                "constraint": "gpu-high",
                "ntasks": 1,
                "cpus-per-task": 1,
                "mem": "32G",
                "time": "48:00:00",
            },
            slurm_flags=[
                "requeue",
            ],
        )
        slurm.run(
            f"""
        {cmd}
        """
        )
    ##
    print("\n")


def main():
    for dataset in all_beir_datasets:
        command = base_command.format(
            alias="openai_msmarco__msl128__100epoch__correct",
            return_best_hypothesis=1,
            num_gen_recursive_steps=50,
            sequence_beam_width=8,
            beam_width=1,
            dataset=dataset,
        )
        run_command(command, "evaluate_corrector")


if __name__ == "__main__":
    main()