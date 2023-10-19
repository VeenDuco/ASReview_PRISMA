# to get asreview data
import shutil
from pathlib import Path
import pandas as pd
from asreview import open_state
from asreview import ASReviewProject
from asreview import ASReviewData

# get the data from the project file
project_path = Path("tmp_data")
# Check if directory exists
if project_path.exists():
    # Remove the existing directory
    shutil.rmtree(project_path)
project_path.mkdir()
project = ASReviewProject.load("BDT.asreview", project_path)

# get the complete dataset
dataset_fp = Path(
    project_path, project.config["id"], "data", project.config["dataset_path"]
)
dataset = ASReviewData.from_file(dataset_fp)
# get state file
with open_state("BDT.asreview") as state:
    df = state.get_dataset()
df.to_csv(project_path / "example_state.csv", index=False)
# extract total number of records that is equal to the number of rows of the dataset
nrecords = len(dataset.to_dataframe())
# how many records are screened
nscreened = len(df)
# how many records have label 1
ninc = df["label"].sum()
# how many records have label 0
nexc = nscreened - ninc


def save_dot_file(filename, grouped_nodes, edges):
    with open(filename, 'w') as f:
        f.write("digraph {\n")
        
        for group in grouped_nodes:
            if len(group) > 1:  # If there's more than one node in the group, rank them the same.
                f.write("    {\n        rank=same\n")
                for node, label, shape in group:
                    f.write(f'        {node} [label="{label}", shape={shape}];\n')
                f.write("    }\n")
            else:
                node, label, shape = group[0]  # If only one node in the group.
                f.write(f'    {node} [label="{label}", shape={shape}];\n')

        for edge in edges:
            f.write(f'    {edge[0]} -> {edge[1]};\n')
            
        f.write("}\n")

grouped_nodes = [
    [('a', '# of studies identified through database searching', 'box'),
     ('b', '# of additional studies identified through other sources', 'box')],
    [('c', f'{nrecords} of studies after duplicates removed', 'box')],
    [('d', f'{nscreened} of studies with title and abstract screened', 'box'),
     ('e', f'{nexc} of studies excluded. {nrecords - nscreened} records not screened.', 'box')],
    [('f', f'{ninc} of full-text articles assessed for eligibility', 'box'),
     ('g', '# of full-text excluded, reasons', 'box')],
    [('h', '# of studies included in qualitative synthesis', 'box'),
     ('i', '# of studies excluded, reasons', 'box')],
    [('j', 'final # of studies included in quantitative synthesis (meta-analysis)', 'box')]
]

edges = ['ac', 'bc', 'cd', 'de','df','fg','fh','hi','hj']

save_dot_file('prisma_graph_output.dot', grouped_nodes, edges)

