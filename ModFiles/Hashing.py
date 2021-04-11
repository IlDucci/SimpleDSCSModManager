import hashlib
import os

from Utils.Path import splitpath

def gather_mod_install_orders(indices):
    results = {}
    for index in indices:
        for rule, data in index.items():
            for filepath, stuff in data.items(): 
                local_filepath = os.path.join(*splitpath(filepath)[3:])
                if local_filepath not in results:
                    results[local_filepath] = []
                results[local_filepath].append((filepath, stuff))
    return results


def hash_file_install_orders(indices):
    buffer_size = 64*1024
    
    result = {}
    mod_install_orders = gather_mod_install_orders(indices)
    for local_filepath, install_order in mod_install_orders.items():
        hasher = hashlib.sha256()
        for filepath, rulebook in install_order:
            with open(filepath, 'rb') as F:
                while True:
                    data = F.read(buffer_size)
                    if not data:
                        break
                    hasher.update(data)
            hasher.update(str(rulebook).encode())
        result[local_filepath] = hasher.hexdigest()
        
    return result

def sort_hashes(hashes_1, hashes_2):
    shared_hashes = []
    for local_filepath, hash_1 in hashes_1.items():
        hash_2 = hashes_2.get(local_filepath)
        if hash_1 == hash_2:
            shared_hashes.append(local_filepath)
    return shared_hashes

def cull_index(indices, files_to_cull):
    for index in indices:
        for key, subindex in index.items():
            if not len(subindex.keys()):
                continue
            first_key = list(subindex.keys())[0]  # Could be any key, would be nice to avoid having to do this massive list conversion
            index_stem = os.path.join(*splitpath(first_key)[:3])
            for local_filepath in files_to_cull:
                index_filepath = os.path.join(index_stem, local_filepath)
                if index_filepath in subindex:
                    del subindex[index_filepath]
                    
    return indices
                
def add_cache_to_index(indices, files_to_add):
    result = {}
    returned_files = []
    for local_filepath in files_to_add:
        new_local_filepath = local_filepath
        for parser in [mbe_parse, script_parse]:
            new_local_filepath = parser(new_local_filepath)
        print(local_filepath, new_local_filepath)
        filepath = os.path.join("output", "cache", "modfiles", new_local_filepath)
        if os.path.exists(filepath):
            returned_files.append(local_filepath)
            result[filepath] = {new_local_filepath: "overwrite"}
            
    indices.append({"mbe": {}, "hca": {}, "script_src": {}, "other": result})
    
    return returned_files

def mbe_parse(name):
    path = splitpath(name)
    if len(path) > 2:
        if path[-2][-3:] == 'mbe':
            return os.path.join(*path[:-1])
    return name

def script_parse(name):
    path = splitpath(name)
    if len(path) >= 2:
        if path[-2] == 'script64' and name[-3:] == 'txt':
            return name[:-3] + 'nut'
    return name