#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    # Create has table
    ht = HashTable(16)
    # Index and insert the hash table
    index = 0
    for weight in weights:
        hash_table_insert(ht, weight, index)
        index += 1
    for weight in weights:
        # weight to find
        target_weight = limit - weight
        target_index = hash_table_retrieve(ht, target_weight)
        if target_index is not None:
            hash_table_remove(ht, target_weight)
            weight_index = hash_table_retrieve(ht, weight)
            if weight_index is None:
                weight_index = 0
            print([target_index, weight_index])
            return [target_index, weight_index]

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
