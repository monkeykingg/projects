class LinkedListNode:
    """
    Node to be used in linked list

    === Attributes ===
    @param LinkedListNode next_: successor to this LinkedListNode
    @param object value: data this LinkedListNode represents
    """
    def __init__(self, value, next_=None):
        """
        Create LinkedListNode self with data value and successor next_.

        @param LinkedListNode self: this LinkedListNode
        @param object value: data of this linked list node
        @param LinkedListNode|None next_: successor to this LinkedListNode.
        @rtype: None
        """
        self.value, self.next_ = value, next_

    def __str__(self):
        """
        Return a user-friendly representation of this LinkedListNode.

        @param LinkedListNode self: this LinkedListNode
        @rtype: str

        >>> n = LinkedListNode(5, LinkedListNode(7))
        >>> print(n)
        5 -> 7 ->|
        """
        # start with a string s to represent current node.
        s = "{} ->".format(self.value)
        # create a reference to "walk" along the list
        current_node = self.next_
        # for each subsequent node in the list, build s
        while current_node is not None:
            s += " {} ->".format(current_node.value)
            current_node = current_node.next_
        # add "|" at the end of the list
        assert current_node is None, "unexpected non_None!!!"
        s += "|"
        return s

    def __eq__(self, other):
        """
        Return whether LinkedListNode self is equivalent to other.

        @param LinkedListNode self: this LinkedListNode
        @param LinkedListNode|object other: object to compare to self.
        @rtype: bool

        >>> LinkedListNode(5).__eq__(5)
        False
        >>> n1 = LinkedListNode(5, LinkedListNode(7))
        >>> n2 = LinkedListNode(5, LinkedListNode(7, None))
        >>> n1.__eq__(n2)
        True
        """
        return (type(self) == type(other) and
                self.value == other.value and
                self.next_ == other.next_)



class LinkedList:
    """
    Collection of LinkedListNodes

    === Attributes ==
    @param: LinkedListNode front: first node of this LinkedList
    @param LinkedListNode back: last node of this LinkedList
    @param int size: number of nodes in this LinkedList
                        a non-negative integer
    """
    def __init__(self):
        """
        Create an empty linked list.

        @param LinkedList self: this LinkedList
        @rtype: None
        """
        self.front, self.back, self.size = None, None, 0

    def __str__(self):
        """
        Return a human-friendly string representation of
        LinkedList self.

        @param LinkedList self: this LinkedList

        >>> lnk = LinkedList()
        >>> print(lnk)
        I'm so empty... experiencing existential angst!!!
        """
        # deal with the case where this list is empty
        if self.front is None:
            assert self.back is None and self.size is 0, "ooooops!"
            return "I'm so empty... experiencing existential angst!!!"
        else:
            # use front.__str__() if this list isn't empty
            return str(self.front)

    def __eq__(self, other):
        """
        Return whether LinkedList self is equivalent to
        other.

        @param LinkedList self: this LinkedList
        @param LinkedList|object other: object to compare to self
        @rtype: bool

        >>> LinkedList().__eq__(None)
        False
        >>> lnk = LinkedList()
        >>> lnk.prepend(5)
        >>> lnk2 = LinkedList()
        >>> lnk2.prepend(5)
        >>> lnk.__eq__(lnk2)
        True
        """
        return (type(self) == type(other) and
                self.front == other.front and
                self.back == other.back and
                self.size == other.size)


    def delete_after(self, value):
        """
        Remove the node following the first occurrence of value, if
        possible, otherwise leave self unchanged.

        @param LinkedList self: this LinkedList
        @param object value: value just before the deletion
        @rtype: None
        """
        node = self.front

        while node.next_ != None:
            if node.next_.next_ == None:
                node.next_ = None
                self.size -= 1
            elif node.value == value:
                node_after = node.next_.next_
                node.next_ = node_after
                self.size -= 1

    def append(self, value):
        """
        Insert a new LinkedListNode with value after self.back.

        @param LinkedList self: this LinkedList.
        @param object value: value of new LinkedListNode
        @rtype: None

        >>> lnk = LinkedList()
        >>> lnk.append(5)
        >>> lnk.size
        1
        >>> print(lnk.front)
        5 ->|
        >>> lnk.append(6)
        >>> lnk.size
        2
        >>> print(lnk.front)
        5 -> 6 ->|
        """
        # create the new node
        new_node = LinkedListNode(value)
        # if the list is empty, the new node is front and back
        if self.size == 0:
            assert self.back is None and self.front is None, "ooops"
            self.front = self.back = new_node
        # if the list isn't empty, front stays the same
        else:
            # change *old* self.back.next_ first!!!!
            self.back.next_ = new_node
            self.back = new_node
        # remember to increase the size
        self.size += 1

    def prepend(self, value):
        """
        Insert value before LinkedList self.front.

        @param LinkedList self: this LinkedList
        @param object value: value for new LinkedList.front
        @rtype: None

        >>> lnk = LinkedList()
        >>> lnk.prepend(0)
        >>> lnk.prepend(1)
        >>> lnk.prepend(2)
        >>> str(lnk.front)
        '2 -> 1 -> 0 ->|'
        >>> lnk.size
        3
        """
        # Create new node with next_ referring to front
        new_node = LinkedListNode(value, self.front)
        # change front
        self.front = new_node
        # if the list was empty, change back
        if self.size == 0:
            self.back = new_node
        # update size
        self.size += 1

    def delete_front(self):
        """
        Delete LinkedListNode self.front from self.

        Assume self.front is not None

        @param LinkedList self: this LinkedList
        @rtype: None

        >>> lnk = LinkedList()
        >>> lnk.prepend(0)
        >>> lnk.prepend(1)
        >>> lnk.prepend(2)
        >>> lnk.delete_front()
        >>> str(lnk.front)
        '1 -> 0 ->|'
        >>> lnk.size
        2
        >>> lnk.delete_front()
        >>> lnk.delete_front()
        >>> str(lnk.front)
        'None'
        """
        assert self.front is not None, "unexpected None!"
        # if back == front, set it to None
        if self.front == self.back:
            self.back = None
        # set front to its successor
        self.front = self.front.next_
        # decrease size
        self.size -= 1

    def __setitem__(self, index, value):
        """
        Set the value of list at position index to value. Raise IndexError
        if index >= self.size

        @param LinkedList self: this LinkedList
        @param index int: position of list to change
        @param object value: new value for linked list
        @rtype: None
        """
        node = self.front

        if index >= self.size:
            raise IndexError()

        if index == 0:
            node.value = value
        elif index == (self.size - 1):
            self.back.value = value
        else:
            for i in range(self.size):
                node = node.next_
                if i == index:
                    node.value = value


    def __add__(self, other):
        """
        Return a new list by concatenating self to other.  Leave
        both self and other unchanged.

        @param LinkedList self: this LinkedList
        @param LinkedList other: Linked list to concatenate to self
        @rtype: LinkedList

        >>> lnk1 = LinkedList()
        >>> lnk1.prepend(5)
        >>> lnk2 = LinkedList()
        >>> lnk2.prepend(7)
        >>> print(lnk1 + lnk2)
        5 -> 7 ->|
        """
        lnk = LinkedList()
        node1 = self.front
        node2 = other.front

        if self.size != 0:
            for i in range(self.size):
                lnk.append(node1.value)
                node1 = node1.next_

        if other.size != 0:
            for i in range(other.size):
                lnk.append(node2.value)
                node2 = node2.next_

        return lnk


    def insert_before(self, value1, value2):
        """
        Insert value1 into LinkedList self before the first occurrence
        of value2, if it exists.  Otherwise leave self unchanged.

        @param LinkedList self: this LinkedList
        @param object value1: value to insert, if possible
        @param object value2: value to insert value1 ahead of
        @rtype: None
        """
        node = self.front
        node1 = LinkedListNode()
        node1.value = value2

        if self.size != 0:
            while node.next_.value != value1 and node.next_ != None:
                node = node.next_
            old_node = node.next_
            node.next_ = node1
            node1.next_ = old_node

    def copy(self):
        """
        Return a copy of LinkedList self.  The copy should have
        different nodes, but equivalent values, from self.

        @param LinkedList self: this LinkedList
        @rtype: LinkedList

        >>> lnk = LinkedList()
        >>> lnk.prepend(5)
        >>> lnk.prepend(7)
        >>> print(lnk.copy())
        7 -> 5 ->|
        """
        pass

    def __len__(self):
        """
        Return the number of nodes in LinkedList self.

        @param LinkedList self: this LinkedList
        @rtype: int
        """
        pass

    def __getitem__(self, index):
        """
        Return the value at LinkedList self's position index.

        @param LinkedList self: this LinkedList
        @param int index: position to retrieve value from
        @rtype: object

        >>> lnk = LinkedList()
        >>> lnk.append(1)
        >>> lnk.append(0)
        >>> lnk.__getitem__(1)
        0
        >>> lnk[-1]
        0
        """
        # deal with a negative index by adding self.size
        while index < 0:
            index += self.size
        if index >= self.size or self.size == 0:
            raise IndexError("index too big!!!")
        # an empty list, or an index that is too large is an error
        else:
            current_node = self.front
            # walk index steps along from 0 to retrieve element
            for step in range(index):
                current_node = current_node.next_
                assert current_node is not None, "unexpected None!!!!!"
            # return the value at position index
            return current_node.value

    def __contains__(self, value):
        """
        Return whether LinkedList self contains value.

        @param LinkedList self: this LinkedList.
        @param object value: value to search for in self
        @rtype: bool

        >>> lnk = LinkedList()
        >>> lnk.append(0)
        >>> lnk.append(1)
        >>> lnk.append(2)
        >>> 2 in lnk
        True
        >>> lnk.__contains__(3)
        False
        """
        current_node = self.front
        # "walk" the linked list
        while current_node is not None:
            # if any node has a value == value, return True
            if current_node.value == value:
                return True
            current_node = current_node.next_
        # if you get to the end without finding value,
        # return False
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()
