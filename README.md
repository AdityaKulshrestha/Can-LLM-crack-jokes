# Can LLM generate novel jokes?

[Research Paper Reference](https://arxiv.org/pdf/2409.03733)

[Detailed Plan](https://docs.google.com/document/d/1lb-un6E5n7taW-eLQkRflvfeNLfnjYpPz188FfzjR24/edit?tab=t.0) 

## Steps to reproduce
### Product random topics for jokes
1. python prepare_dataset.py

### Producing baseline results
1. python baseline.py
2. evaluate.py

### Producing Plansearch results
1. python plansearch.py
2. evaluate.py      # Change the evaluated_response filename

 
## Observation

![Average Scores](assests/joke_scores_plot.png)

![Average Scores](assests/joke_Clarity_plot.png)

![Average Scores](assests/joke_Originality_plot.png)

![Average Scores](assests/joke_Surprise_Element_plot.png)

![Average Scores](assests/joke_Timing_and_Structure_plot.png)
