from graphviz import Digraph # to create the graph
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
print(nrecords, nscreened, ninc, nexc)


pri = Digraph()
with pri.subgraph() as c:
    c.attr(rank='same')
    c.node('a', '# of studies identified through database searching', shape='box')
    c.node('b', '# of additional studies identified through other sources', shape='box')
pri.node('c', f'{nrecords} of studies after duplicates removed', shape='box')
with pri.subgraph() as c:
    c.attr(rank='same')
    c.node('d', f'{nscreened} of studies with title and abstract screened', shape='box')
    c.node('e', f'{nexc} of studies excluded. {nrecords - nscreened} records not screened.', shape='box')
with pri.subgraph() as c:
    c.attr(rank='same')
    c.node('f', f'{ninc} of full-text articles assessed for eligibility', shape='box')
    c.node('g', '# of full-text excluded, reasons', shape='box')
with pri.subgraph() as c:
    c.attr(rank='same')
    c.node('h', '# of studies included in qualitative synthesis', shape='box')
    c.node('i', '# of studies excluded, reasons', shape='box')
pri.node('j', 'final # of studies included in quantitative synthesis (meta-analysis)', shape='box')
pri.edges(['ac', 'bc', 'cd', 'de','df','fg','fh','hi','hj'])
pri.render(view=True)
pri.save('graph_output.dot')
