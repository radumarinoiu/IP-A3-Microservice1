from flask import jsonify

task_diff_for_period = {
    "hard": "tired",
    "easy": "relaxed"
}


def sortTasks(data):
    preferences = data["preferences"]
    tasks = data["tasks"]
    sortedTasks = {
        "morning": [],
        "afternoon": [],
        "evening": []
    }

    sortedPreferences = {
        "relaxed": [],
        "tired": []
    }

    for pref in preferences:
        if preferences[pref] in sortedPreferences:
            sortedPreferences[preferences[pref]].append(pref)

    for pref in sortedPreferences:
        temp_tasks = []
        if sortedPreferences[pref]:
            for task in tasks:
                if task["priority"] in task_diff_for_period and \
                        task_diff_for_period[task["priority"]] == pref:
                    temp_tasks.append(task)
            while temp_tasks:
                for period in sortedPreferences[pref]:
                    if not temp_tasks:
                        break
                    sortedTasks[period].append(temp_tasks.pop())

    return jsonify(sortedTasks), 200
