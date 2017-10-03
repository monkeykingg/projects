from stack import Stack

def list_stack(lst, sta):
    """(list, stack) -> None

    @param lst:
    @type lst:
    @param sta:
    @type sta:
    @return:
    @rtype:
    """
    for item in lst:
        sta.add(item)
    while not sta.is_empty():
        remove_item = sta.remove()
        if not isinstance(remove_item, list):
            print(remove_item)
        else:
            for element in remove_item:
                sta.add(element)

if __name__ == '__main__':
    stack1 = Stack()
    item = input("Type a sring:")
    while item != 'end':
        stack1.add(item)
        item = input("Type a sring:")
    while not stack1.is_empty():
        stack1.remove()
