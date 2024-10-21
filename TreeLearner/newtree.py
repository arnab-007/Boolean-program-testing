from z3 import *
import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt





# nov = 5
# '''Read the DistEstimate_counterexample file and store the values in a list. Finally convert each decimal value to binary and store in above variables'''

# def convert_to_binary(line):
#     line = line.strip().split()
#     binary_representation = bin(int(line[0]))[2:].zfill(5)
#     return [int(i) for i in binary_representation]

# def get_counter_examples(positive=True, negative=True):
#     positive_counter_examples = []
#     negative_counter_examples = []
#     if positive:
#         with open("DistEstimate_counterexamples", "r") as f:
#             lines = f.readlines()
#             for line in lines:
#                 positive_counter_examples.append(convert_to_binary(line))
#     if negative:
#         with open("Validifier_counterexamples", "r") as f:
#             lines = f.readlines()
#             for line in lines:
#                 negative_counter_examples.append(convert_to_binary(line))
#     return positive_counter_examples, negative_counter_examples


# positive_counter_examples, negative_counter_examples = get_counter_examples()
# positive_df = pd.DataFrame(positive_counter_examples, columns=[f'x{i}' for i in range(1, nov+1)])
# negative_df = pd.DataFrame(negative_counter_examples, columns=[f'x{i}' for i in range(1, nov+1)])

# # Add labels (1 for positive, 0 for negative)
# positive_df['label'] = 1
# negative_df['label'] = 0

# # Combine the two DataFrames
# final_df = pd.concat([positive_df, negative_df], ignore_index=True)

# print(final_df)

# X = final_df.drop('label', axis=1)
# Y = final_df['label']

# # Fit the decision tree
# clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=12, random_state=0)
# clf = clf.fit(X, Y)



# plt.figure(figsize=(20,10))
# tree.plot_tree(clf, filled=True, feature_names=X.columns, class_names=['0', '1'], rounded=True, fontsize=14)
# plt.show()
