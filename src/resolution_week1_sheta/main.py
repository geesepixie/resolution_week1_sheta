import argparse
import sys          # hash include basically
import os
import json 
import datetime

TASKS_FILE = "tasks.json"

def load_tasks():  
    if not os.path.exists(TASKS_FILE): #file exists?
        return []    #empty array (I MEAN LIST, FOCUS)
    with open(TASKS_FILE, "r") as file: #read mood, hence r
        return json.load(file)
    
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file: #write mood, hence w
        json.dump(tasks, file, indent=2)

def main():
    parser = argparse.ArgumentParser()   # class object (?)
    parser.add_argument("task", type=str, nargs="?", help="Task to add") # positional argument

    parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
    parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
    parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
    parser.add_argument("-s", "--search", type=str, help="Search tasks by keyword")
    parser.add_argument("--clear", help="Delete all tasks", action="store_true")
    parser.add_argument("--daily", help="Make task recur daily", action="store_true")

    args = parser.parse_args()

    if len(sys.argv) == 1: #is the argument passed?
        parser.print_help(sys.stderr) 
        sys.exit(1) #error
        

    # - - - - - - - - - - - - - - - - - - -     
    if args.list:
        tasks = load_tasks()
        if not tasks:
            print("No tasks found :(")
            sys.exit(0)
        for task in tasks:
            status = "✔" if task["done"] else " "
            due = f" (due {task['due']})" if "due" in task else ""
            print(f"[{status}] {task['id']}: {task['task']}{due}")
        sys.exit(0)
    # - - - - - - - - - - - - - - - - - - -
    elif args.search:
        tasks = load_tasks()
        found = False

        for task in tasks:
            if args.search.lower() in task["task"].lower():
                status = "✔" if task["done"] else " "
                due = f" (due {task['due']})" if "due" in task else ""
                print(f"[{status}] {task['id']}: {task['task']}{due}")
                found = True

        if not found:
            print("No matching tasks found.")
    # - - - - - - - - - - - - - - - - - - -
    elif args.clear:
        confirm = input("Are you sure you want to delete all tasks? (yay/nay): ")

        if confirm.lower() in ("yay", "y", "yes"):
            save_tasks([])
            print("All tasks have been cleared :O")
        else:
            print("Clear cancelled :D")
    # - - - - - - - - - - - - - - - - - - -
    elif args.complete:
        tasks = load_tasks()
        found = False

        for task in tasks:
            if task["id"] == args.complete:
                found = True

                if not task["done"]:
                    task["done"] = True

                    # recurring tasks
                    if task.get("recurring") == "daily":
                        new_id = max(t["id"] for t in tasks) + 1 if tasks else 1

                        new_task = {
                            "id": new_id,
                            "task": task["task"],
                            "done": False,
                            "recurring": "daily",
                            "due": (
                                datetime.datetime.now()
                                + datetime.timedelta(days=1)
                            ).date().isoformat(),
                        }

                        tasks.append(new_task)

                save_tasks(tasks)
                print(f"Task {args.complete} marked as complete")
                break

        if not found:
            print("Task ID not found.")
    # - - - - - - - - - - - - - - - - - - -
    elif args.delete:
        tasks = load_tasks()
        new_tasks = []
        deleted = False

        for task in tasks:
            if task["id"] != args.delete:
                new_tasks.append(task)
            else:
                deleted = True

        if deleted:
            save_tasks(new_tasks)
            print(f"Task with ID of {args.delete} deleted")
        else:
            print("Task ID not found.")
    # - - - - - - - - - - - - - - - - - - -
    elif args.task:
        tasks = load_tasks()

        new_id = max(task["id"] for task in tasks) + 1 if tasks else 1

        new_task = {
            "id": new_id,
            "task": args.task,
            "done": False,
        }

        if args.daily:
            new_task["recurring"] = "daily"
            new_task["due"] = datetime.datetime.now().date().isoformat()

        tasks.append(new_task)
        save_tasks(tasks)

        print(f"Task '{args.task}' added with ID of {new_id}")

if __name__ == "__main__":
    main()