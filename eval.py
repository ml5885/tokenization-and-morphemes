def run_eval(golds, preds):
   tp = 0
   fp = 0
   fn = 0
   for g, p in zip(golds, preds):
      g_bag = g.strip().split(" ")
      p_bag = p.strip().split(" ")
      tp += sum([1 for i in p_bag if i in g_bag])
      fp += sum([1 for i in p_bag if not i in g_bag])
      fn += sum([1 for i in g_bag if not i in p_bag])
   precision = tp / (tp + fp)
   recall = tp / (tp + fn)
   if precision == 0 or recall == 0:
      f1 = 0
   else:
      f1 = 2 / ((1/precision) + (1/recall))
   return f1