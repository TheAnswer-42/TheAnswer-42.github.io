import heapq
from util import read_osm_data, great_circle_distance, to_local_kml_url

ALLOWED_HIGHWAY_TYPES = {
    'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified',
    'residential', 'living_street', 'motorway_link', 'trunk_link',
    'primary_link', 'secondary_link', 'tertiary_link',
}


DEFAULT_SPEED_LIMIT_MPH = {
    'motorway': 60,
    'trunk': 45,
    'primary': 35,
    'secondary': 30,
    'residential': 25,
    'tertiary': 25,
    'unclassified': 25,
    'living_street': 10,

    'motorway_link': 30,
    'trunk_link': 30,
    'primary_link': 30,
    'secondary_link': 30,
    'tertiary_link': 25,
}

def build_auxiliary_structures(nodes_filename, ways_filename):
    max_speed_limit = float('-inf')

    adjacency = {}
    node_locs = {}
    for way in read_osm_data(ways_filename):
        if way['tags'].get('highway', None) in ALLOWED_HIGHWAY_TYPES:
            twoway = way['tags'].get('oneway', 'no') != 'yes'
            if way['nodes'][0] not in adjacency:
                adjacency[way['nodes'][0]] = set()

            if 'maxspeed_mph' in way['tags']:
                speedlimit = way['tags']['maxspeed_mph']
            else:
                speedlimit = DEFAULT_SPEED_LIMIT_MPH[way['tags']['highway']]
            if speedlimit > max_speed_limit:
                max_speed_limit = speedlimit
            for first, second in zip(way['nodes'], way['nodes'][1:]):
                adjacency.setdefault(first, set()).add((second, speedlimit))
                if second not in adjacency:
                    adjacency[second] = set()
                if twoway:
                    adjacency[second].add((first, speedlimit))

    for node in read_osm_data(nodes_filename):
        if node['id'] in adjacency:
            node_locs[node['id']] = (node['lat'], node['lon'])

    return node_locs, adjacency, max_speed_limit


def trace_path(node):
    reverse_path = []
    while node is not None:
        reverse_path.append(node[0])
        node = node[1]
    return reverse_path[::-1]


def a_star(adjacency, start_state, end_state, cost_func, heuristic):
    expanded = set()
    agenda = []
    heapq.heappush(agenda, (0, 0, (start_state, None)))
    while agenda:
        _, cost, node = heapq.heappop(agenda)

        state = node[0]

        # if we've already expanded this state, just move on; nothing to be
        # gained from doing it again...
        if state in expanded:
            continue

        #if we're done, return a path
        if state == end_state:
            return trace_path(node)

        # otherwise, add this state to expanded, and add children to the
        # agenda.
        expanded.add(state)
        if state not in adjacency:
            continue
        for child in adjacency[state]:
            if child[0] in expanded:
                # short-circuit here: if this child has already been expanded,
                # don't even bother putting it in the agenda.
                continue
            new_cost = cost + cost_func(state, child)
            priority = new_cost + heuristic(child[0])
            heapq.heappush(agenda, (priority, new_cost, (child[0], node)))

    # no more agenda; stop
    return None

def nearest_node_to_loc(node_locs, loc):
    best = float('inf')
    node = None
    for id_, nloc in node_locs.items():
        dist = great_circle_distance(loc, nloc)
        if dist < best:
            best = dist
            node = id_
    return node


def find_short_path(aux_structures, loc1, loc2):
    """
    loc1 and loc2 are (lat, lon) tuples
    """
    node_locs, adjacency, max_speed_limit = aux_structures

    node1 = nearest_node_to_loc(node_locs, loc1)
    node2 = nearest_node_to_loc(node_locs, loc2)

    print('running search')
    path = a_star(adjacency, node1, node2,
                  cost_func=lambda n1, n2: great_circle_distance(node_locs[n1], node_locs[n2[0]]),
                  heuristic=lambda node: great_circle_distance(node_locs[node], node_locs[node2]))
    return [node_locs[n] for n in path] if path is not None else None


def find_fast_path(aux_structures, loc1, loc2):
    """
    loc1 and loc2 are (lat, lon) tuples
    """
    node_locs, adjacency, max_speed_limit = aux_structures

    node1 = nearest_node_to_loc(node_locs, loc1)
    node2 = nearest_node_to_loc(node_locs, loc2)


    print('running search')
    path = a_star(adjacency, node1, node2,
                  cost_func=lambda n1, n2: great_circle_distance(node_locs[n1], node_locs[n2[0]])/n2[1],
                  heuristic=lambda node: great_circle_distance(node_locs[node], node_locs[node2])/max_speed_limit)
    return [node_locs[n] for n in path] if path is not None else None
