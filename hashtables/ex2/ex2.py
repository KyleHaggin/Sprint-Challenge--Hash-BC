#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length
    output = []

    # Insert tickets into hash table
    for ticket in tickets:
        hash_table_insert(hashtable, ticket.source, ticket.destination)

    # Begin from none and add rest to list
    key = 'NONE'
    value = hash_table_retrieve(hashtable, key)

    while value != 'NONE':
        output.append(value)
        key = value
        value = hash_table_retrieve(hashtable, key)

    return output
