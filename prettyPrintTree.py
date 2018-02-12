from deap import gp

def decode(expression):
   if expression == 'add':
       return '+'
   if expression == 'mul':
       return '*'
   if expression == 'truediv':
       return '/'
   if expression == 'sqrt':
       return 'sqrt'
   if expression == 'log':
       return 'ln'
   if expression == 'ARG0':
       return 'child_win_score'
   if expression == 'ARG1':
       return 'child_visit_count'
   if expression == 'ARG2':
       return 'current_visit_count'
   
   return expression

def prettyPrint(tree):
   subject = tree[0].name
   decoding = decode(subject)
   if len(decoding) > 4 or len(tree) < 2:
       return decoding

   if decoding == 'ln' or decoding == 'sqrt':
       subtree_slice_1 = tree.searchSubtree(1)
       #print (subtree_slice_1)

       return decoding + "(" + prettyPrint(gp.PrimitiveTree(tree[subtree_slice_1.start:subtree_slice_1.stop])) + ")"

   subtree_slice_1 = tree.searchSubtree(1)
   subtree_slice_2 = tree.searchSubtree(subtree_slice_1.stop)
   
   return "(" + prettyPrint(gp.PrimitiveTree(tree[subtree_slice_1.start:subtree_slice_1.stop])) + " " + decoding + " " + prettyPrint(gp.PrimitiveTree(tree[subtree_slice_2.start:subtree_slice_2.stop])) + ")"

#print (prettyPrint(gp.PrimitiveTree.from_string('add(truediv(child_win_score, child_visit_count), (mul(1.414,sqrt(mul(2.0,truediv(log(current_visit_count),child_visit_count))))) )', pset)))