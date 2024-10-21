from TreeLearner import CustomDecisionTree
import pandas as pd
import copy
import random
import time
import os

PATH = os.path.realpath("")

def get_ratio(tree_copy, mutation, leaf, distCurr, validCurr):
    if mutation == 'split':
        try:
            '''If trying to split a leaf node that has only one datapoint, it will raise a ValueError.
            In this case, we would like to discard this move and try another one.'''
            tree_copy.split_node(leaf)
        except ValueError:
            return None
        error_bounds = tree_copy.get_error_bounds()
        gaindist = distCurr - error_bounds['dist_error']
        gainvalid = validCurr - error_bounds['valid_error']
        move = ((gaindist+gainvalid)/2, tree_copy, error_bounds['dist_error'], error_bounds['valid_error'])
        return move
    elif mutation == 'prune':
        try:
            '''If trying to prune the root node that is the only node in the tree, it will raise a ValueError.'''
            tree_copy.prune_node(leaf)
        except ValueError:
            return None
        error_bounds = tree_copy.get_error_bounds()
        gaindist = distCurr - error_bounds['dist_error']
        gainvalid = validCurr - error_bounds['valid_error']
        move = ((gaindist+gainvalid), tree_copy, error_bounds['dist_error'], error_bounds['valid_error'])
        return move






#MuteTree(tree, dataset, distCurr, validCurr)
def MuteTree(tree, df, distUser, validUser, iteration):
    start = time.time()
    predictions = tree.predict(df[list(df.columns[:-3])].values, expected_labels=df['label'].values, weights=df['weight'].values, member=df['member'].values)
    #tree.print_leaf_datapoints()
    print(predictions)
    tree.save_tree(output_file='tree_on_new_data')
    error_bounds = tree.get_error_bounds()
    print(error_bounds)
    distCurr, validCurr = error_bounds['dist_error'], error_bounds['valid_error']
    set_of_mutations = ['split', 'prune']
    #tree.save_tree(output_file='ondata2')
    while((distCurr > distUser or validCurr > validUser) and time.time() - start < 100):
        leaf_ids = tree.get_all_leaf_nodes()
        moves = []
        for mutation in set_of_mutations:
            for leaf in leaf_ids:
                #print(f'{mutation=}, {leaf=}')
                tree_copy = copy.deepcopy(tree)
                move = get_ratio(tree_copy, mutation, leaf, distCurr, validCurr)
                if move:
                    moves.append(move)
        moves.sort(key=lambda x: x[0], reverse=True)
        _, tree, distCurr, validCurr = random.choice(moves[:4])
        #print(distCurr,validCurr)
        # tree.save_tree(output_file=f'intermediate_tree_{iteration}')
    #print(moves)
    if distCurr <= distUser  and validCurr <= validUser:
        
        print(f'Total time taken for iteration {iteration}: {time.time() - start}')
        print(distCurr,validCurr)
        print("Final Error Bounds: ", tree.get_error_bounds())
        tree.save_tree(output_file=f'{PATH}/final_trees/final_tree_{iteration}')








initial_data = {'a': [0,1,1,1,1,1,0,0],
    'b': [0,1,1,1,0,0,1,1],
    'c': [1,0,0,1,1,0,0,1],
    'd': [0,1,1,0,1,0,1,1],
    'e': [0,0,1,1,0,1,0,1],
    'label': [1,1,1,1,0,0,0,0],
    'weight': [1,1,1,1,1,1,1,1],
    'member': [0,1,1,1,0,0,0,0]}

data2 = {'a': [0,1,1,0,0],
    'b': [1,0,0,0,0],
    'c': [1,0,0,0,0],
    'd': [0,0,1,1,1],
    'e': [0,0,0,0,1],
    'label': [1,1,1,0,0],
    'weight': [1,1,1,1,1],
    'member': [1,1,1,0,0]}





df = pd.DataFrame(initial_data)
X = df[['a', 'b', 'c', 'd', 'e']].values
y = df['label'].values
clf = CustomDecisionTree(max_depth=6)
clf.fit(X, y, feature_names=df.columns[:-3])
clf.save_tree(output_file='initial_tree')
predictions = clf.predict(X, expected_labels=y, weights=df['weight'].values, member=df['member'].values)
print(predictions)
print(X,y)
df2 = pd.DataFrame(data2)
X_test = df2[['a', 'b', 'c', 'd', 'e']].values
y_test = df2['label'].values
print(X_test,y_test)

for iteration in range(2):
    clf_copy = copy.deepcopy(clf)
    print(f'{iteration=}')
    random.seed(iteration + 10)
    MuteTree(clf_copy, pd.DataFrame(data2), 3, 0, iteration)











'''
complete_data = {'a': [0,0,0,1,1,0,1,1,1,1,1,0,0,0,0,1],
                 'b': [0,0,0,0,0,1,0,1,1,1,1,0,1,1,1,0],
                 'c': [0,0,1,0,0,1,1,0,0,1,1,1,0,0,1,1],
                 'd': [0,1,0,0,1,1,1,0,1,0,1,1,0,1,0,0],
                 'label': [0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0]
}

complete_df = pd.DataFrame(complete_data)
X = complete_df[['a', 'b', 'c', 'd']].values
y = complete_df['label'].values
complete_clf = CustomDecisionTree(max_depth=6)
complete_clf.fit(X, y, feature_names=complete_df.columns[:-1])
complete_clf.save_tree(output_file='complete_tree')



# member is 1 if datapoint is obtained from DistEstimate and 0 if is obtained from Validifier
data = {
    'a': [1, 1, 1, 0, 0, 1],
    'b': [1, 1, 1, 0, 1, 0],
    'c': [0, 0, 1, 0, 1, 0],
    'd': [0, 1, 0, 0, 0, 1],
    'label': [1, 1, 1, 0, 0, 0],
    'weight': [1, 1, 1, 1, 1, 1],
    'member': [1, 1, 1, 0, 0, 0]
}
data2 = {
    'a': [0,0,0,0,1],
    'b': [0,1,0,1,1],
    'c': [1,1,0,0,1],
    'd': [1,1,1,1,1],
    'label': [1,1,0,0,1],
    'weight': [1, 1, 1, 1, 1],
    'member': [1, 1, 0, 0, 0]
}


'''