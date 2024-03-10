import json
import os
from argparse import ArgumentParser

from llm_orchestrator.verifier import Verifier


def main():
    parser = ArgumentParser()

    predictions_folder_default = os.path.join(".", "data", "test_set", "predictions", "json_data")
    ground_truth_folder_default = os.path.join(".", "data", "test_set", "ground_truths")
    schema_dir_default = os.path.join(".", "data", "json_schemas")
    report_path_default = os.path.join(".", "data", "test_set", "predictions", "report.txt")

    parser.add_argument("--predictions_folder", default=predictions_folder_default)
    parser.add_argument("--ground_truth_folder", default=ground_truth_folder_default)
    parser.add_argument("--schema_dir", default=schema_dir_default)
    parser.add_argument("--report_path", default=report_path_default)
    args = parser.parse_args()

    verifier = Verifier(args.schema_dir)

    pred_files = os.listdir(args.predictions_folder)
    gt_files = os.listdir(args.ground_truth_folder)
    pred_files.sort(key=lambda name: int(name.split("_")[1].split(".")[0]))
    gt_files.sort(key=lambda name: int(name.split("_")[1].split(".")[0]))
    error_report = []
    for pred_file, ground_truth_file in zip(pred_files, gt_files):
        error_report.append(f"Comparing {pred_file} vs {ground_truth_file}")
        pred_path = os.path.join(args.predictions_folder, pred_file)
        ground_truth_path = os.path.join(args.ground_truth_folder, ground_truth_file)
        with open(pred_path) as f:
            pred = json.load(f)
        with open(ground_truth_path) as f:
            ground_truth = json.load(f)
        score, error = verifier.score(pred, ground_truth)
        error_report.append(f"Score for {pred_file} vs {ground_truth_file}: {score}, error: {error}\n")

    print("\n".join(error_report))


if __name__ == "__main__":
    main()
