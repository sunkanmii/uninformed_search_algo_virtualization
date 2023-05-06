def dfids():
    root = get_root()
    res = float("inf")
 
    def dfids_search(node, depth, limit):
        if depth <= limit and node is not None:
            val = node.val
            if val == 12:
                nonlocal res
                res = min(res, depth)
            else:
                dfids_search(node.left, depth + 1, limit)
                dfids_search(node.right, depth + 1, limit)
 
    for limit in range(1,5):
        dfids_search(root, 0, limit)
        if res < float("inf"):
            return res
    return -1

if __name__ == "__main__":
   print("\nShortest Depth: ", dfids())