import json
import os
import argparse
from datetime import datetime

Task_file = "tasks.json"

# Load tasks from JSON
def load_tasks():
    if not os.path.exists(Task_file):
        return []
    with open(Task_file, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Save tasks to JSON
def save_tasks(tasks):
    with open(Task_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

# Add a new task
def add_tasks(description):
    tasks = load_tasks()
    new_id = 1 if not tasks else max(task["id"] for task in tasks) + 1
    now = datetime.now().isoformat(timespec="seconds")

    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task {new_id} was added: {description}")

# Delete a task by ID
def delete_task(task_id):
    tasks = load_tasks()
    task_to_delete = next((t for t in tasks if t["id"] == task_id), None)

    if not task_to_delete:
        print(f"Not found task with ID {task_id}")
        return

    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"✅ Task {task_id} was deleted")

# update task
def update_task(task_id, new_description):
    tasks = load_tasks()
    task_to_update = next((t for t in tasks if t["id"] == task_id), None)

    if not task_to_update:
        print(f"not found tast with id{task_id}")
        return
    task_to_update["description"] = new_description
    task_to_update["updatedAt"] = datetime.now().isoformat(timespec="seconds")

    save_tasks(tasks)
    print(f"Task{task_id} was updated: {new_description}")

# mark task
def mark_task(task_id, new_status):
    tasks = load_tasks()
    task_to_mark = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task_to_mark:
        print(f"not found task with ID {task_id}")
        return

    if new_status not in ["todo", "in-progress", "done"]:
        print(f"Invalid status: {new_status}")
        return

    task_to_mark["status"] = new_status
    task_to_mark["updatedAt"] = datetime.now().isoformat(timespec="seconds")

    save_tasks(tasks)
    print(f"Task {task_id} was updated status: {new_status}")


# List tasks
def list_task(status=None):
    tasks = load_tasks()
    if not tasks:
        print("have not any task in the list")
        return

    if status:
        tasks = [t for t in tasks if t["status"] == status]
        if not tasks:
            print(f"Not have task with status {status} ")
            return
        
    print("List of tasks:")
    for t in tasks:
        print(f"[{t['id']}] {t['description']} - {t['status']} (created: {t['createdAt']}, updated: {t['updatedAt']})")

# menu
def menu():
    while True:
        print("\n=== Task Tracker Menu ===")
        print("1. Add task")
        print("2. Delete task")
        print("3. Update task")
        print("4. Mark task status")
        print("5. List tasks")
        print("6. Exit")

        ch = input("Enter your choice")

        if ch == "1":
            desc = input("Enter task description: ")
            add_tasks(desc)
        elif ch == "2":
            tid = int(input("Enter task ID to delete: "))
            delete_task(tid)
        elif ch == "3":
            tid = int(input("Enter task ID to update: "))
            desc = input("Enter new description: ")
            update_task(tid, desc)
        elif ch == "4":
            tid = int(input("Enter task ID to mark: "))
            status = input("Enter new status (todo/in-progress/done): ")
            mark_task(tid, status)
        elif ch == "5":
            status = input("Enter status filter (todo/in-progress/done or leave blank): ")
            list_task(status if status else None)
        elif ch == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
 


def main():
    parser = argparse.ArgumentParser(prog="task-cli", description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add", help="Thêm task mới")
    add_parser.add_argument("description", type=str, help="Mô tả công việc")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Xóa task theo ID")
    delete_parser.add_argument("id", type=int, help="ID của task cần xóa")

    #update
    update_parser = subparsers.add_parser("update", help="cập nhật task theo ID")
    update_parser.add_argument("id", type = int, help = "ID của task cần cập nhật")
    update_parser.add_argument("description", type = str, help = "task mới")

    # list
    list_parser = subparsers.add_parser("list", help="Liệt kê tasks")
    list_parser.add_argument("status", type=str, nargs="?", choices=["todo", "in-progress", "done"],
                             help="Lọc theo trạng thái (tùy chọn)")

    # mark
    mark_parser = subparsers.add_parser("mark", help="Đổi trạng thái task theo ID")
    mark_parser.add_argument("id", type=int, help="ID của task cần đổi trạng thái")
    mark_parser.add_argument("status", type=str, choices=["todo", "in-progress", "done"],
                             help="Trạng thái mới (todo, in-progress, done)")
    
    # menu
    subparsers.add_parser("menu", help="Chạy menu tương tác")

    args = parser.parse_args()

    if args.command == "add":
        add_tasks(args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "list":
        list_task(args.status)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "mark":
        mark_task(args.id, args.status)
    elif args.command == "menu":
        menu()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
