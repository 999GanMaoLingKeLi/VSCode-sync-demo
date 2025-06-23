#测试修改上传代码class node:
class node:    
    def __init__(self,val):
            self.val=val
            self.next=None
            self.pre=None
class MyLinkedList:

    def __init__(self):
        self.size=0
        self.head,self.tail=node(0),node(0)
        self.head.next=self.tail
        self.tail.pre=self.head
    def get(self, index: int) -> int:
        if index<0 or index>=self.size:
            return -1
        if index+1<self.size-index:
            cur=self.head
            for _ in range(index+1):
                cur=cur.next
        else:
            cur=self.tail
            for _ in range(self.size-index):
                cur=cur.pre
        return cur.val
    def addAtHead(self, val: int) -> None:
        self.addAtIndex(0,val)

    def addAtTail(self, val: int) -> None:
        self.addAtIndex(self.size,val)

    def addAtIndex(self, index: int, val: int) -> None:
        if index>self.size:
            return
        index=max(0,index)
        if index<self.size-index:
            pred=self.head
            for _ in range(index):
                pred=pred.next
            succ=pred.next
        else:
            succ=self.tail
            for _ in range(self.size-index):
                succ=succ.pre
            pred=succ.pre
        self.size+=1
        to_add=node(val)
        to_add.pre=pred
        to_add.next=succ
        pred.next=to_add
        succ.pre=to_add
    def deleteAtIndex(self, index: int) -> None:
        if index<0 or index>=self.size:
            return
        if index<self.size-index:
            pred=self.head
            for _ in range(index):
                pred=pred.next
            succ=pred.next.next
        else:
            succ=self.tail
            for _ in range(self.size-index-1):
                succ=succ.pre
            pred=succ.pre.pre
        self.size-=1
        pred.next=succ
        succ.pre=pred


# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)