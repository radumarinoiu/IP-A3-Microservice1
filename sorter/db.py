from flask import jsonify
import json

task_priority_index = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}


def sortTasks(data):
    preferences = data["preferences"]
    tasks = data["tasks"]
    sorted_filtered_tasks = {
        "Low": [],
        "Medium": [],
        "High": []
    }

    final_periods = {
        "morning": [],
        "afternoon": [],
        "evening": []
    }

    final_priorities = {
        "Low": [],
        "Medium": [],
        "High": []
    }

    for priority in sorted_filtered_tasks:
        new_list = []
        for task in tasks:
            if task_priority_index[task["priority"]] <= task_priority_index[priority]:
                new_list.append(task)
        deadline_sorted_list = sorted(new_list, key=lambda k: k['deadline'])
        sorted_filtered_tasks[priority] = sorted(
            deadline_sorted_list,
            key=lambda k: task_priority_index[k['priority']],
            reverse=True
        )

    for pref in preferences:
        if preferences[pref] in final_priorities:
            final_priorities[preferences[pref]].append(pref)

    last_list_len = 0
    while last_list_len != len(sorted_filtered_tasks["High"]):
        last_list_len = len(sorted_filtered_tasks["High"])
        for priority in final_priorities:
            for period in final_priorities[priority]:
                if sorted_filtered_tasks[priority]:
                    final_periods[period].append(sorted_filtered_tasks[priority].pop(0))
                    for prio in sorted_filtered_tasks:
                        try:
                            sorted_filtered_tasks[prio].remove(final_periods[period][-1])
                        except Exception:
                            pass

    print json.dumps(final_periods, indent = 4)

    return jsonify(final_periods), 200
