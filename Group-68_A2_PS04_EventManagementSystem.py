class AvlNode:
    def __init__(self, event_ID="", start_time="", end_time="", event_name = ""):
        self.event_ID = event_ID
        self.event_name = event_name
        self.start_time = start_time
        self.end_time = end_time
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
        self.Node = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def insert(self, root,  event_ID="", start_time="", end_time="", event_name=""):
        if not root:
            return AvlNode(event_ID, start_time, end_time, event_name)
        elif int(event_ID) < int(root.event_ID):
            root.left = self.insert(root.left, event_ID, start_time, end_time, event_name)
        else:
            root.right = self.insert(root.right, event_ID, start_time, end_time, event_name)

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        # Left rotation
        if balance > 1 and int(event_ID) < int(root.left.event_ID):
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and int(event_ID) > int(root.right.event_ID):
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and int(event_ID) > int(root.left.event_ID):
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and int(event_ID) < int(root.right.event_ID):
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        self.root = root
        return root

    def delete(self, root, event_ID):
        if not root:
            print("returned root")
            return root
        print("int(event_ID) = ", int(event_ID))
        if int(event_ID) < int(root.event_ID):
            root.left = self.delete(root.left, event_ID)
        elif event_ID > root.event_ID:
            root.right = self.delete(root.right, event_ID)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp

            temp = self.min_value_node(root.right)
            root.event_ID = temp.event_ID
            root.right = self.delete(root.right, temp.event_ID)

        if not root:
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)

        # Left rotation
        if balance > 1 and self.balance(root.left) >= 0:
            return self.right_rotate(root)

        # Right rotation
        if balance < -1 and self.balance(root.right) <= 0:
            return self.left_rotate(root)

        # Left-Right rotation
        if balance > 1 and self.balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right-Left rotation
        if balance < -1 and self.balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))

        return y

    def min_value_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    def search(self, root, event_ID):
        if not root or int(root.event_ID) == int(event_ID):
            return root

        if int(root.event_ID) < int(event_ID):
            return self.search(root.right, event_ID)
        elif int(root.event_ID) > int(event_ID):
            return self.search(root.left, event_ID)

        else:
            if int(root.event_ID) == int(event_ID):
                return root
            else:
                return ""

    def searchByRange(self, root, event_ID):
        if not root or root.event_ID == event_ID:
            return root

        if int(root.event_ID) == int(event_ID):
            return root
        elif int(root.event_ID) < int(event_ID):
            return self.search(root.right, event_ID)
        elif int(root.event_ID) > int(event_ID):
            return self.search(root.left, event_ID)

        else:
            return ""

    def addEvent(self, event_ID, start_time, end_time, event_name):
        self.root = self.insert(self.root, event_ID, start_time, end_time, event_name)
        write_output("Added Book: " + event_ID + " - " + event_name)

    def removeEvent(self, event_ID):
        node = self.search(self.root, event_ID)

        if not node:
            write_output(f"Error: Event " + str(event_ID) + " doesnot exist")
        else:
            self.root = self.delete(self.root, event_ID)
            print("self.root.event_name in removed = ", self.root.event_name)
            write_output("Removed Book: " + self.root.event_ID + " - " + self.root.event_name)


    def searchEvent(self, event_ID):
        self.root = self.search(self.root, event_ID)
        write_output("Searched : " + self.root.event_ID )
        write_output("---------------------------------------------------------------------------------------------------- " )
        write_output(self.root.event_ID + " - " + self.root.start_time +" - "+ self.root.end_time + " - "+ self.root.event_name)
        write_output("---------------------------------------------------------------------------------------------------- " )

    def searchEventByRange(self, start_time="", end_time=""):
        print(" event by range")




def write_output(message):
    f.write(message +"\n")


f = open("outputPS04.txt", "w")
avl = AVLTree()

if __name__ == "__main__":
    # Read input file
    inputfile = open("inputPS04.txt", "r")

    while True:
        command = inputfile.readline()
        if not command:
            break
        action = command.split(":")[0].strip()

        if action == "Add Event":
            event_info = command.split(":", 1)[1]

            event_ID = event_info.split("-")[0]
            start_time = event_info.split("-")[1]
            end_time = event_info.split("-")[2]
            event_name = event_info.split("-")[3]
            avl.addEvent(event_ID, start_time, end_time, event_name)

        elif action == "Remove Event":
            event_info = command.split(":", 1)[1]
            event_ID = event_info.split("-")[0]
            node = avl.removeEvent(event_ID)

        elif action == "Search Event by ID":
            event_info = command.split(":", 1)[1]
            event_ID = event_info.split("-")[0]
            avl.searchEvent(event_ID)

        elif action == "Search Event by Range":
            event_info = command.split(":", 1)[1]
            event_ID = event_info.split("-")[0]
            write_output("Book Details for ID " + event_ID + ": \n")
            # event_ID = 'Yes' if bookNode.available else 'No'
            # write_output(
            #     "-" + bookNode.title + " by " + bookNode.author + ", ISBN: " + bookNode.isbn.strip() + ", Available: " + event_ID + "\n")

        else:
            write_output("Error: Please enter valid action: \n \t \t "
                         "addBook, borrowBook, returnBook, checkBook, listAvailableBooks, \n "
                         "\t \t listBooksByAuthor, listPatronsBooks, removeBook ")

    def inorder_traversal(root):
        if root:
            inorder_traversal(root.left)
            print(root.event_ID),
            inorder_traversal(root.right)


    inorder_traversal(avl.root)

    f.close()

