# ASReview_PRISMA
Create a PRISMA Flowchart and fill it with data from .asreview file

For now there are two scripts. "flowchart.py" works with graphviz and produces a pdf and .dot file. 

Since this creates potentially new dependencies and the flowchart is not filled anyway we can only produce a .dot file. 
This is done in "flowchart_nodependencies.py". This data can then be used to update and print online for instance using https://dreampuf.github.io/GraphvizOnline/