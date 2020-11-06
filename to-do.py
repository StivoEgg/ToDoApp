import os
import click
import csv

csvPath = './todos.csv'

class todoItem:
    def __init__(self, itemId, title, priority):
        self.id = str(itemId)
        self.title = title
        self.priority = int(priority)

def getAllTodos():
    items = []
    
    mode = 'r' if os.path.exists(csvPath) else 'w+'
    with open(csvPath, mode) as f:
        reader = csv.reader(f)
        for row in reader:
            items.append(todoItem(row[0], row[1], row[2]))
    return items

def saveAllTodos(items):
    with open(csvPath, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for item in items:
            writer.writerow([item.id, item.title, item.priority])
    displayAllTodos(allTodos)

def displayAllTodos(items):
    print("ID, Title, Priority")
    for item in allTodos:
        print (", ".join([item.id, item.title, str(item.priority)]))
    printMissingPrioritiesMessage(allTodos)

def printMissingPrioritiesMessage(items):
    missingPriorities = list(range(1, items[-1].priority))
    for item in items[:-1]:
        if item.priority in missingPriorities:
            missingPriorities.remove(item.priority)
    if len(missingPriorities) > 0:
        print("The following priorities are missing: " + ", ".join([str(p) for p in missingPriorities] ))

@click.group()
def cli():
    pass

@click.command('list')
def listTodos():
    displayAllTodos(allTodos)

@click.command('add')
@click.argument('title')
@click.argument('priority')
def addTodo(title, priority):
    newItem = todoItem(len(allTodos), title, priority)
    allTodos.append(newItem)
    saveAllTodos(allTodos)
    
@click.command('delete')
@click.argument('targetid')
def deleteTodo(targetid):
    target = None
    for item in allTodos:
        if (item.id == targetid):
            target = item
            break
    if target is None:
        print("Cannot find item with ID: " + targetid)
    else:
        allTodos.remove(target)
        print("Successfully deleted item with ID: " + targetid)
        saveAllTodos(allTodos)

if __name__ =="__main__":
    cli.add_command(addTodo)
    cli.add_command(listTodos)
    cli.add_command(deleteTodo)
    allTodos = getAllTodos()
    allTodos.sort(key=lambda x : x.priority, reverse=False)
    cli()
