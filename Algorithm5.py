#!/usr/bin/python
# -*- coding: utf-8 -*-
import readData as rd
import pickle
from time import clock
from heapq import heappush, heappop
import pp


def _weight_function(G, weight):
    """Returns a function that returns the weight of an edge.
    The returned function is specifically suitable for input to
    functions :func:`_dijkstra` and :func:`_bellman_ford_relaxation`.
    Parameters
    ----------
    G : NetworkX graph.
    weight : string or function
        If it is callable, `weight` itself is returned. If it is a string,
        it is assumed to be the name of the edge attribute that represents
        the weight of an edge. In that case, a function is returned that
        gets the edge weight according to the specified edge attribute.
    Returns
    -------
    function
        This function returns a callable that accepts exactly three inputs:
        a node, an node adjacent to the first one, and the edge attribute
        dictionary for the eedge joining those nodes. That function returns
        a number representing the weight of an edge.
    If `G` is a multigraph, and `weight` is not callable, the
    minimum edge weight over all parallel edges is returned. If any edge
    does not have an attribute with key `weight`, it is assumed to
    have weight one.
    """
    if callable(weight):
        return weight
    # If the weight keyword argument is not callable, we assume it is a
    # string representing the edge attribute containing the weight of
    # the edge.
    if G.is_multigraph():
        return lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
    return lambda u, v, data: data.get(weight, 1)


def _dijkstra_multisource(G, sources, Cset,weight,pred=None, cutoff=None, target=None):
    """Uses Dijkstra's algorithm to find shortest weighted paths
    Parameters
    ----------
    G : NetworkX graph
    sources : non-empty iterable of nodes
        Starting nodes for paths. If this is just an iterable containing
        a single node, then all paths computed by this function will
        start from that node. If there are two or more nodes in this
        iterable, the computed paths may begin from any one of the start
        nodes.
    weight: function
        Function with (u, v, data) input that returns that edges weight
    pred: dict of lists, optional(default=None)
        dict to store a list of predecessors keyed by that node
        If None, predecessors are not stored.
    paths: dict, optional (default=None)
        dict to store the path list from source to each node, keyed by node.
        If None, paths are not stored.
    target : node label, optional
        Ending node for path. Search is halted when target is found.
    cutoff : integer or float, optional
        Depth to stop the search. Only return paths with length <= cutoff.
    Returns
    -------
    distance : dictionary
        A mapping from node to shortest distance to that node from one
        of the source nodes.
    Notes
    -----
    The optional predecessor and path dictionaries can be accessed by
    the caller through the original pred and paths objects passed
    as arguments. No need to explicitly return pred or paths.
    """
    weight = _weight_function(G, weight)
    if not sources:
        raise ValueError('sources must not be empty')
    if target in sources:
        return ({target: 0}, {target: [target]})
    weight = _weight_function(G, weight)
    paths = {source: [source] for source in sources}  # dictionary of paths
    G_succ = G.succ if G.is_directed() else G.adj
    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {}
    in_c = {}
    # fringe is heapq with 3-tuples (distance,depth,mark,node)
    fringe = []
    for source in sources:
        seen[source] = 0
        in_c[source] = 1
        push(fringe, (0, 0, source))
    while fringe:
    	flag = 1
    	for x in in_c:
    		flag = in_c[x] and flag
    		if not flag:
    			break
        (d, dpt, v) = pop(fringe)
        if flag and v!= source:
    		break
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        if v == target:
            break
        for u, e in G_succ[v].items():
            cost = weight(v, u, e)
            if cost is None:
                continue
            vu_dist = dist[v] + cost
            vu_dpt = dpt + 1
            if cutoff is not None:
                if vu_dpt > cutoff:
                    continue
            if u in dist:
                if vu_dist < dist[u]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                in_c[u] = in_c[v] and (u in Cset)
                push(fringe, (vu_dist, vu_dpt, u))
                if paths is not None:
                    paths[u] = paths[v] + [u]
                if pred is not None:
                    pred[u] = [v]
            elif vu_dist == seen[u]:
                if pred is not None:
                    pred[u].append(v)
        del in_c[v]

    # The optional predecessor and path dictionaries can be accessed
    # by the caller via the pred and paths objects passed as arguments.
    return dist, paths


def kShortestPathCpver(k, G):
	C = set(G.nodes())
	kspc_dist = {}
	for v in G.nodes():
		C.remove(v)
		v_dist, v_tree = _dijkstra_multisource(G, [v], C,weight='weight', cutoff=k)
		flag = 1
		for w in v_tree:
			if flag:
				if w != v and w in C:
					w_dist, w_tree = _dijkstra_multisource(G, [w], C,weight='weight', cutoff=k)
					for x in w_tree:
						if (v in set(w_tree[x])) and (len(w_tree[x]) - 1 >= k) and (not (set(w_tree[x]) - set([w]) & C)):
							C.add(v)
							kspc_dist[v] = v_dist
							flag = 0
							break
			else:
				break
	return C, kspc_dist


def areaConstruction(k, G):
	start = clock()
	kSpc, kspc_dist = kShortestPathCpver(k, G)
	end = clock()
	print '=======', k, '========'
	print 'kspc time', end - start
	print 'kspc num', len(kSpc)
	print 'rest num', len(set(G.nodes()) - kSpc)
	area = {}
	radius = {}
	areadict = {}
	nospc_dist = {}
	start = clock()
	for u in kSpc:
		area[u] = set([u])
		areadict[u] = u
		radius[u] = 0
	nospc = list(set(G.nodes()) - kSpc)
	spc = list(kSpc)
	nospc.sort()
	spc.sort()
	for v in spc:
		for u in kspc_dist[v]:
			if u not in nospc_dist or kspc_dist[v][u] < nospc_dist[u]:
				nospc_dist[u] = kspc_dist[v][u]
				areadict[u] = v
	for u in areadict:
		if areadict[u] not in radius or nospc_dist[u] >radius[areadict[u]]:
			radius[areadict[u]] = nospc_dist[u]
	end = clock()
	print 'pair time', end - start
	# filename = 'data/area-' + str(k) + '.txt'
	# pickle.dump(area, open(filename, 'w'))
	filename = 'data/areadict-' + str(k) + '.npy'
	pickle.dump(areadict, open(filename, 'w'))
	filename = 'data/areaR-' + str(k) + '.npy'
	pickle.dump(radius, open(filename, 'w'))
	print 'write area data'
	print len(area)
	return area, areadict, radius

if __name__ == "__main__":
    G = rd.readRoad('data/50_graph.txt')
    print 'G.node num', len(G.nodes())
    print 'G.edges num', len(G.edges())
    ncores = 2
    if ncores > 1:
	    jobs = []
	    job_server = pp.Server(5)
	    for ki in [5, 10, 20, 50,100]:
	    	jobs.append(job_server.submit(areaConstruction, (ki, G), (kShortestPathCpver, _dijkstra_multisource, _weight_function),
	    	            ('import networkx as nx', 'from heapq import heappush, heappop', 'import readData as rd', 'from time import clock')))
	    print 'job begin'
	    job_server.wait()
	    print 'job end'
    else:
    	areaConstruction(3,G)