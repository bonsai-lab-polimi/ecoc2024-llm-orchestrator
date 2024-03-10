import json
import os

from llm_orchestrator.verifier import Verifier


def main():
    predictions_folder = os.path.join(".", "data", "test_set", "predictions", "json_data")
    ground_truth_folder = os.path.join(".", "data", "test_set", "ground_truths")
    schema_dir = os.path.join(".", "data", "json_schemas")
    verifier = Verifier(schema_dir)

    pred_files = os.listdir(predictions_folder)
    gt_files = os.listdir(ground_truth_folder)
    pred_files.sort()
    gt_files.sort()
    for pred_file, ground_truth_file in zip(pred_files, gt_files):
        pred_path = os.path.join(predictions_folder, pred_file)
        ground_truth_path = os.path.join(ground_truth_folder, ground_truth_file)
        with open(pred_path) as f:
            pred = json.load(f)
        with open(ground_truth_path) as f:
            ground_truth = json.load(f)
        score, error = verifier.score(pred, ground_truth)
        print(f"Score for {pred_file} vs {ground_truth_file}: {score}, error: {error}")


if __name__ == "__main__":
    main()

