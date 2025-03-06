import os
import json
import glob
import subprocess
from collections import defaultdict

def parse_results(directory):
    data = defaultdict(dict)

    for model_dir in os.listdir(directory):
        model_path = os.path.join(directory, model_dir)
        if not os.path.isdir(model_path):
            continue

        for json_file in glob.glob(os.path.join(model_path, "*.json")):
            with open(json_file, "r") as f:
                try:
                    content = json.load(f)
                    for task, scores in content.get("results", {}).items():
                        if model_dir not in data[task]:
                            data[task][model_dir] = {}
                        data[task][model_dir].update(scores)
                except Exception as e:
                    print(e, f)

    return data

def generate_html(results, output_file="results.html"):
    with open(output_file, "w") as f:
        f.write("<html><head><title>Model Results</title></head><body>")

        for task, models in results.items():
            f.write(f"<h2>Task: {task}</h2>")

            # Collect all possible score keys
            all_metrics = set()
            for model_scores in models.values():
                all_metrics.update(model_scores.keys())
            all_metrics -= {"alias"}  # Remove alias key if present
            all_metrics = sorted(all_metrics)

            # Write table header
            f.write("<table border='1'><tr><th>Model</th>")
            for metric in all_metrics:
                f.write(f"<th>{metric}</th>")
            f.write("</tr>")

            # Write table rows
            for model, scores in models.items():
                f.write(f"<tr><td>{model}</td>")
                for metric in all_metrics:
                    f.write(f"<td>{scores.get(metric, 'N/A')}</td>")
                f.write("</tr>")

            f.write("</table><br>")

        f.write("</body></html>")

def commit_to_branch(branch_name, output_file):

    results_data = parse_results("../results")
    command = f"""
    cd ..
    git checkout {branch_name}
    """
    subprocess.run(command, shell=True, check=True)

    generate_html(results_data, output_file)
    subprocess.run(f"git add {output_file}", shell=True, check=True)
    subprocess.run(f"git commit -m 'Update {output_file}'", shell=True, check=True)
    subprocess.run(f"git push origin {branch_name}", shell=True, check=True)

if __name__ == "__main__":
    branch_name = "leaderboard"
    output_file = "index.html"
    commit_to_branch(branch_name, output_file)

