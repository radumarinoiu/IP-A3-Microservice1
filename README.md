
# IP A3 Microservice1
This REST microservice is providing access to tasks, their assignment, and more similar features.
### Usage:

| Method | Route | Action |
| ------ | ------ | ------ |
| GET | /tasks | Get all album ids |
| GET | /tasks/`task_id` | Get task with id `task_id` |
|  |  |  |
| POST | /tasks | Creates a new task using json `{}` and returns it's id |
|  |  |  |
| PUT | /tasks/`task_id` | Modifies task with id `task_id` updating it's content using json `{}` |
|  |  |  |
| DELETE | /tasks/`task_id` | Delete task with id `task_id` |

| Method | Route | Action |
| ------ | ------ | ------ |
| GET | /assigner | Get all album ids |
| GET | /assigner/`assignment_id` | Get assignment with id `assignment_id` |
|  |  |  |
| POST | /assigner | Creates a new assignment using json `{}` and returns it's id |
|  |  |  |
| PUT | /assigner/`assignment_id` | Modifies assignment with id `assignment_id` updating it's content using json `{}` |
|  |  |  |
| DELETE | /assigner/`assignment_id` | Delete assignment with id `assignment_id` |
