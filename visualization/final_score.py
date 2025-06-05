import matplotlib.pyplot as plt
import json


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def plot_avg_score(basedata, plansearch_data, plot_name, title):
    x = range(len(basedata[0]))
    avg_baseline = [round(((a + b + c + d)/4), 2) for a, b, c, d in zip(basedata[0], basedata[1], basedata[2], basedata[3])]
    avg_plansearch = [round(((a + b + c + d)/4), 2) for a, b, c, d in zip(plansearch_data[0], plansearch_data[1], plansearch_data[2], plansearch_data[3])]


    plt.plot(x, avg_baseline, label='Baseline Score')
    plt.plot(x, avg_plansearch, label='PlanSearch')
    # plt.plot(x, basedata[2], label='Gemini')
    # plt.plot(x, basedata[3], label='Qwen')
    # plt.plot(x, avg, label='Average Score')

    plt.xlabel("Jokes")
    plt.ylabel("Scores (0-5)")
    plt.title(title)
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_name)
    plt.clf()
    plt.close()



def main():
    baseline_file = "eval_response/baseline_evaluation.json"
    plan_search_file = "eval_response/plan_search_jokes_evaluation.json"

    baseline_data = read_json_file(baseline_file)
    plan_search_data = read_json_file(plan_search_file)

    baseline_scores = [[], [], [], []]
    for idx in baseline_data:
        for i in range(len(idx['quality_score'])):
            key = "Final_Score" if "Final_Score" in idx['quality_score'][i].keys() else "Final Score"
            baseline_scores[i].append(idx['quality_score'][i][key])

    plan_search_scores = [[], [], [], []]
    for idx in plan_search_data:
        for i in range(len(idx['quality_score'])):
            key = "Final_Score" if "Final_Score" in idx['quality_score'][i].keys() else "Final Score"
            plan_search_scores[i].append(idx['quality_score'][i][key])

    plot_avg_score(baseline_scores, plan_search_scores, "assests/joke_scores_plot.png", "Average Score")

    baseline_scores = [[], [], [], []]
    for idx in baseline_data:
        for i in range(len(idx['quality_score'])):
            key = "Surprise_Element"
            baseline_scores[i].append(idx['quality_score'][i][key])

    plan_search_scores = [[], [], [], []]
    for idx in plan_search_data:
        for i in range(len(idx['quality_score'])):
            key = "Surprise_Element"
            plan_search_scores[i].append(idx['quality_score'][i][key])

    plot_avg_score(baseline_scores, plan_search_scores, f"assests/joke_{key}_plot.png", "Surprise Element Score")

    baseline_scores = [[], [], [], []]
    for idx in baseline_data:
        for i in range(len(idx['quality_score'])):
            key = "Originality"
            baseline_scores[i].append(idx['quality_score'][i][key])

    plan_search_scores = [[], [], [], []]
    for idx in plan_search_data:
        for i in range(len(idx['quality_score'])):
            key = "Originality"
            plan_search_scores[i].append(idx['quality_score'][i][key])

    plot_avg_score(baseline_scores, plan_search_scores, f"assests/joke_{key}_plot.png", "Originality Score")

    baseline_scores = [[], [], [], []]
    for idx in baseline_data:
        for i in range(len(idx['quality_score'])):
            key = "Timing_and_Structure"
            baseline_scores[i].append(idx['quality_score'][i][key])

    plan_search_scores = [[], [], [], []]
    for idx in plan_search_data:
        for i in range(len(idx['quality_score'])):
            key = "Timing_and_Structure"
            plan_search_scores[i].append(idx['quality_score'][i][key])

    plot_avg_score(baseline_scores, plan_search_scores, f"assests/joke_{key}_plot.png", "Timing and Structure Score")

    baseline_scores = [[], [], [], []]
    for idx in baseline_data:
        for i in range(len(idx['quality_score'])):
            key = "Impact"
            baseline_scores[i].append(idx['quality_score'][i][key])

    plan_search_scores = [[], [], [], []]
    for idx in plan_search_data:
        for i in range(len(idx['quality_score'])):
            key = "Impact"
            plan_search_scores[i].append(idx['quality_score'][i][key])

    plot_avg_score(baseline_scores, plan_search_scores, f"assests/joke_{key}_plot.png", "Impact Score")

    baseline_scores = [[], [], [], []]
    for idx in baseline_data:
        for i in range(len(idx['quality_score'])):
            key = "Clarity"
            baseline_scores[i].append(idx['quality_score'][i][key])

    plan_search_scores = [[], [], [], []]
    for idx in plan_search_data:
        for i in range(len(idx['quality_score'])):
            key = "Clarity"
            plan_search_scores[i].append(idx['quality_score'][i][key])

    plot_avg_score(baseline_scores, plan_search_scores, f"assests/joke_{key}_plot.png", "Clarity scores")


if __name__ == "__main__":
    main()
