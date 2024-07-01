import time

import Api_key
import meilisearch


def main():
    client = meilisearch.Client("http://localhost:7700", Api_key.MASTER_KEY)
    index = str(input("Which index do you want to update? "))
    limit = int(input("What should the new limit be? "))

    # set a limit for the index - 20k is good enough
    task = client.index(index).update_pagination_settings({"maxTotalHits": limit})
    print(task.task_uid)

    # disable typo allowance
    client.index(index).update_typo_tolerance({"enabled": False})

    # add Cited number and Published to the sortable attributes
    task = client.index(index).update_sortable_attributes(["Cited number", "Published"])
    check_status(client, task)

    # update the ranking rules --> moved sort higher up
    task = client.index(index).update_ranking_rules(
        ["words", "sort", "typo", "proximity", "attribute", "exactness"]
    )
    check_status(client, task)

    print("Settings updated")


def check_status(client, task):
    """
    tracks the status of the task and only returns when the task failed or is finished

    Needed atm to not spam the server with too many tasks -> might not be needed in a future
    version of meilisearch
    """

    task_id = task.task_uid

    while task.status == "enqueued" or task.status == "processing":
        time.sleep(2)  # we use sleep to avoid spamming the server with status requests
        task = client.get_task(task_id)

    if task.status == "failed":
        print(f"Failed to process task {task_id}, check meilisearch console")
        return

    return


if __name__ == "__main__":
    main()
