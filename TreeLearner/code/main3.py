import numpy as np
import pandas as pd
from collections import Counter

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, *, value=None, node_id=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        self.data_points = pd.DataFrame()
        self.node_id = node_id

    def is_leaf_node(self):
        return self.value is not None

class CustomDecisionTree:
    def __init__(self, min_samples_split=2, max_depth=100):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.root = None
        self.node_counter = 0
        self.features_used = set()

    def fit(self, X, y, feature_names=None):
        self.feature_names = feature_names if feature_names is not None else [f'feature_{i}' for i in range(X.shape[1])]
        self.root = self._grow_tree(X, y, used_features=set())
        return list(self.features_used)

    def _grow_tree(self, X, y, depth=0, used_features=None):
        if used_features is None:
            used_features = set()
        
        num_samples, num_features = X.shape
        num_labels = len(np.unique(y))
        node_id = self.node_counter
        self.node_counter += 1

        if (depth >= self.max_depth or num_labels == 1 or num_samples < self.min_samples_split):
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value, node_id=node_id)

        best_feature, best_threshold = self._best_split(X, y, num_features, used_features)

        if best_feature is None:
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value, node_id=node_id)

        used_features.add(best_feature)
        self.features_used.add(self.feature_names[best_feature])

        left_indices = X[:, best_feature] <= best_threshold
        right_indices = X[:, best_feature] > best_threshold
        
        left = self._grow_tree(X[left_indices], y[left_indices], depth + 1, set(used_features))
        right = self._grow_tree(X[right_indices], y[right_indices], depth + 1, set(used_features))
        return Node(feature=best_feature, threshold=best_threshold, left=left, right=right, node_id=node_id)

    def _best_split(self, X, y, num_features, used_features):
        best_gain = -1
        split_idx, split_threshold = None, None

        for feature_idx in range(num_features):
            if feature_idx in used_features:
                continue

            thresholds = np.unique(X[:, feature_idx])
            for threshold in thresholds:
                gain = self._information_gain(X, y, feature_idx, threshold)

                if gain > best_gain:
                    best_gain = gain
                    split_idx = feature_idx
                    split_threshold = threshold

        return split_idx, split_threshold

    def _information_gain(self, X, y, feature_idx, threshold):
        parent_entropy = self._entropy(y)
        left_indices = X[:, feature_idx] <= threshold
        right_indices = X[:, feature_idx] > threshold
        if len(left_indices) == 0 or len(right_indices) == 0:
            return 0

        n = len(y)
        n_left, n_right = len(y[left_indices]), len(y[right_indices])
        e_left, e_right = self._entropy(y[left_indices]), self._entropy(y[right_indices])
        child_entropy = (n_left / n) * e_left + (n_right / n) * e_right

        ig = parent_entropy - child_entropy
        return ig

    def _entropy(self, y):
        hist = np.bincount(y)
        ps = hist / len(y)
        return -np.sum([p * np.log2(p) for p in ps if p > 0])

    def _most_common_label(self, y):
        counter = Counter(y)
        most_common = counter.most_common(1)[0][0]
        return most_common

    def predict(self, X, original_labels=None):
        predictions = []
        if original_labels is None:
            original_labels = [None] * len(X)
        for x, original_label in zip(X, original_labels):
            leaf = self._traverse_tree_and_store(x, original_label, self.root)
            predictions.append(leaf.value)
        return np.array(predictions)

    def _traverse_tree_and_store(self, x, original_label, node):
        if node.is_leaf_node():
            data_point = pd.DataFrame([np.append(x, original_label)], columns=list(self.feature_names) + ['label'])
            node.data_points = pd.concat([node.data_points, data_point], ignore_index=True)
            return node

        if x[node.feature] <= node.threshold:
            return self._traverse_tree_and_store(x, original_label, node.left)
        return self._traverse_tree_and_store(x, original_label, node.right)

    def print_leaf_data(self):
        def _print_leaf_data(node):
            if node.is_leaf_node():
                print(f"Leaf Node ID: {node.node_id} - Predicted Value: {node.value}, Data Points:\n{node.data_points}\n")
            else:
                _print_leaf_data(node.left)
                _print_leaf_data(node.right)

        _print_leaf_data(self.root)
    
    def print_tree(self):
        def _print_tree(node, depth=0):
            if node is None:
                return
            if node.is_leaf_node():
                print(f"{'|   ' * depth}Leaf Node(ID: {node.node_id}, Value: {node.value})")
            else:
                print(f"{'|   ' * depth}Node(ID: {node.node_id}, Feature: {self.feature_names[node.feature]}, Threshold: {node.threshold})")
                _print_tree(node.left, depth + 1)
                _print_tree(node.right, depth + 1)

        _print_tree(self.root)

def prune_mutation(tree, node_id_to_prune):
    def find_node_and_parent(node, node_id, parent=None):
        if node is None:
            return None, None
        if node.node_id == node_id:
            return node, parent
        left_result = find_node_and_parent(node.left, node_id, node)
        if left_result[0] is not None:
            return left_result
        return find_node_and_parent(node.right, node_id, node)

    node_to_prune, parent = find_node_and_parent(tree.root, node_id_to_prune)

    if node_to_prune is None:
        print(f"Node with ID {node_id_to_prune} not found.")
        return tree

    sibling = parent.left if parent and parent.right == node_to_prune else parent.right if parent else None
    _, grandparent = find_node_and_parent(tree.root, parent.node_id) if parent else (None, None)

    if sibling and sibling.is_leaf_node():
        combined_data = pd.concat([node_to_prune.data_points, sibling.data_points], ignore_index=True)
        parent.value = tree._most_common_label(combined_data['label'].values)
        parent.data_points = combined_data
        parent.left = None
        parent.right = None
    elif sibling:
        if grandparent is None:
            tree.root = sibling
        else:
            if grandparent.left == parent:
                grandparent.left = sibling
            else:
                grandparent.right = sibling
        tree.predict(node_to_prune.data_points[tree.feature_names].values, original_labels=node_to_prune.data_points['label'].values)

    tree.node_counter = 0
    tree.features_used = set()

    def update_node_ids_and_features(node):
        if node is None:
            return
        node.node_id = tree.node_counter
        tree.node_counter += 1
        if not node.is_leaf_node():
            tree.features_used.add(tree.feature_names[node.feature])
            update_node_ids_and_features(node.left)
            update_node_ids_and_features(node.right)

    update_node_ids_and_features(tree.root)

    return tree




# Sample data
data = {'a': [0,0,0,1,1,1,1,1,0,0,0],
    'b': [0,0,0,1,1,1,0,0,1,1,1],
    'c': [0,0,1,0,0,1,1,0,0,1,1],
    'd': [1,1,0,1,1,0,1,0,1,0,1],
    'e': [0,1,0,0,1,1,0,1,0,0,1],
    'label': [1,1,1,1,1,1,0,0,0,0,0],
    'weight': [0,0,0,0,0,0,0,0,0,0,0],
    'member': [1,1,1,1,1,1,0,0,0,0,0]}

df = pd.DataFrame(data)
X = df[['a', 'b', 'c', 'd', 'e']].values
y = df['label'].values

# Train the custom decision tree
clf = CustomDecisionTree(max_depth=3)
clf.fit(X, y, feature_names=df.columns[:-1])

# Make predictions
predictions = clf.predict(X, original_labels=y)

# Print the dataset at each leaf node
#clf.print_leaf_data()

data2 = {'a': [0,1,1,0,0,0,1],
    'b': [1,0,0,0,0,0,1],
    'c': [1,0,0,0,0,1,1],
    'd': [0,0,1,1,1,0,0],
    'e': [0,0,0,0,1,0,1],
    'label': [1,1,1,0,0,0,0],
    'weight': [1,1,1,1,1,1,1],
    'member': [1,1,1,0,0,0,0]}

df = pd.DataFrame(data2)
X = df[['a', 'b', 'c', 'd', 'e']].values
y = df['label'].values
predictions = clf.predict(X, original_labels=y)


#print("Predictions on data2:", predictions)

# Print the dataset at each leaf node
#clf.print_leaf_data()


# Print the tree]
clf.print_tree()

# Prune the tree
pruned_tree = prune_mutation(clf, 4)
pruned_tree.print_tree()