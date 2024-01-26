import meilisearch
import json


def create_key(client):
    key = client.create_key(
        options={
            "description": "Test-Search: Development API key",
            "actions": ["search"],
            "indexes": ["*"],
            "name": "Search Key - test",
            "expiresAt": None,
        }
    )

    print("KEY: ", key)
    return key


def get_key(client, key_uid):
    key = client.get_key(key_uid)
    print(key)
    return key


def get_keys(client):
    keys = client.get_keys({"limit": 5})
    print(keys)
    return keys


def save_key(key):
    key_dict = {
        "Name": key.name,
        "Description": key.description,
        "UID": str(key.uid),
        "Key": str(key.key),
        "Actions": key.actions,
        "Indexes": key.indexes,
        "Expires at": str(key.expires_at),
        "Created at": str(key.created_at),
        "Updated at": str(key.updated_at),
    }

    with open("new_key.json", "w", encoding="utf-8") as outfile:
        json.dump(key_dict, outfile, indent=2)


def main():
    client = meilisearch.Client("http://localhost:7700", "aSampleMasterKey")

    # create_key(client)

    key_uid = str(input("Please enter the key  UID: "))
    key = get_key(client, key_uid)
    save_key(key)
    # get_keys(client)


if __name__ == "__main__":
    main()
