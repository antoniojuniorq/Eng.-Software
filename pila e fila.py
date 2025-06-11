class PersonalArray:
    SIZE = 5

    def __init__(self):
        self.insertPosition = 0
        self.elements = [None] * self.SIZE

    def isEmpty(self):
        return self.size() == 0
    
    def size(self):
        return self.insertPosition
        
    def isMemoryFull(self):
        return self.insertPosition == len(self.elements)
    
    def append(self, newElement):
        if self.isMemoryFull():
            self.updateMemory()
        self.elements[self.insertPosition] = newElement
        self.insertPosition += 1
    
    def updateMemory(self):
        newArray = [None] * (self.size() + self.SIZE)
        for i in range(self.insertPosition):
            newArray[i] = self.elements[i]
        self.elements = newArray
    
    def clear(self):
        self.elements = [None] * self.SIZE
        self.insertPosition = 0
    
    def remove(self):
        if not self.isEmpty():
            self.insertPosition -= 1
            return self.elements[self.insertPosition]
        return None
    
    def removePosition(self, position):
        if position < 0 or position >= self.insertPosition:
            print("Posição inválida!")
            return None  

        removedElement = self.elements[position]
        
        for i in range(position, self.insertPosition - 1):
            self.elements[i] = self.elements[i + 1]

        self.insertPosition -= 1
        return removedElement  
        
    def insertAt(self, position, newElement):
        if position < 0 or position > self.insertPosition:
            print("Posição inválida!")
            return
        if self.isMemoryFull():
            self.updateMemory()
        for i in range(self.insertPosition, position, -1):
            self.elements[i] = self.elements[i - 1]
        self.elements[position] = newElement
        self.insertPosition += 1   
    
    def elementAt(self, position):
        if position < 0 or position >= self.insertPosition:
            print("Posição inválida!")
            return None
        return self.elements[position]


class PersonalStack:
    def __init__(self):
        self.list = PersonalArray()
    
    def push(self, newElement):
        self.list.append(newElement)
    
    def pop(self):
        return self.list.remove()


class PersonalQueue:
    def __init__(self):
        self.list = PersonalArray()
    
    def enqueue(self, newElement):
        self.list.append(newElement)
    
    def dequeue(self):
        return self.list.removePosition(0)

fila_motoristas = PersonalQueue()

fila_motoristas.enqueue("Motorista Antonio Junior")
fila_motoristas.enqueue("Motorista Antonio Carlos")
fila_motoristas.enqueue("Motorista Roberto")
fila_motoristas.enqueue("Motorista Guilherme")
fila_motoristas.enqueue("Motorista Luis Gonçalves")

pilha_servicos = PersonalStack()

quantidade_servico = [10, 8, 6, 4, 2] 

for servico in quantidade_servico:
    pilha_servicos.push(servico)

while not fila_motoristas.list.isEmpty():
    motorista = fila_motoristas.dequeue()
    servico = pilha_servicos.pop()  
    print(f"{motorista} recebeu {servico} tarefas.")

