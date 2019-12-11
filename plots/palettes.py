from collections        import defaultdict
from palettable.tableau import *
from palettable.colorbrewer.qualitative import *

# =========================================================
# Dictionary containing color sequences for plotting
# =========================================================
colors = defaultdict(lambda: Tableau_10.mpl_colors)
key_val_pairs = [
    ['Pastel1'      , Pastel1_9.mpl_colors],
    ['Pastel2'      , Pastel2_8.mpl_colors],
    ['Set1'         , Set1_9.mpl_colors],
    ['Set2'         , Set2_8.mpl_colors],
    ['Set3'         , Set3_12.mpl_colors],
    ['Tableau'      , Tableau_10.mpl_colors],
    ['TableauLight' , TableauLight_10.mpl_colors],
    ['TableauMedium', TableauMedium_10.mpl_colors],
    ['Custom1'      , [Tableau_10.mpl_colors[i] for i in [3,1,2,0,4]]],
    ['Custom2'      , ['crimson', 'goldenrod', 'forestgreen', 'dodgerblue', 'orchid']]
]
for key, val in key_val_pairs:
    colors[key] = val

# =========================================================
# Dictionary containing line styles for plotting
# =========================================================
linestyles = defaultdict(lambda: ['-', '--', '-.', ':'])
