import json
import Api_key
import meilisearch


def create_key(client):
    """
    Creates a key for meilisearch

    Arguments:  A client connected to the meilisearch database. The connection needs
                to be established with the masterkey!
                Requires the user to input a name, description and date


    By default only creates a key with search priviledges, be careful when handing out
    keys with higher priviledges! Change in the code below if you need a key with more
    priviledges.

    """

    actions = ["search"]
    indexes = ["*"]

    name = str(input("Give a name for the new key: "))
    description = str(input("Give a description for the new key: "))
    expires = str(input("Give an expiration date 'YYYY-MM-DD', leave empty for no expiration: "))

    if len(expires) == 0:
        expires = None
    else:
        expires = expires + "T00:00:00Z"

    print("Do you want to create this key: ")
    print("Name: ", name)
    print("Description: ", description)
    print("Actions: ", actions)
    print("Indexes: ", indexes)
    print("Expires at: ", expires)
    create = str(input("y/n: "))

    if create in ["y", "Y", "Yes", "yes"]:
        key = client.create_key(
            options={
                "name": name,
                "description": description,
                "actions": actions,
                "indexes": indexes,
                "expiresAt": expires,
            }
        )
    else:
        return None

    print("KEY: ", key)
    return key


def get_key(client, key_uid):
    """
    Returns the key-object of the given key_uid

    Arguments:  A connection to the client, established with the master key
                The Key uid of the key that should be returned
    """
    key = client.get_key(key_uid)
    print(key)
    return key


def get_keys(client):
    """
    Returns a list of keys

    Arguments:  A connection to the client, established with the master key

    The limit defines how many keys should be returned, most recent one first
    """
    limit = 5

    keys = client.get_keys({"limit": limit})

    print(keys)

    return keys


def save_key(client, key_uid):
    """
    Saves a key to a json file

    Arguments:  A connection to the client, established with the master key
                The Key uid of the key that should be saved
    """
    filename = "new_key.json"

    key = client.get_key(key_uid)

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

    with open(filename, "w", encoding="utf-8") as outfile:
        json.dump(key_dict, outfile, indent=2)

    print("Key saved to file: ", filename)


def delete_key(client, key_uid):
    """
    Deletes a key

    Arguments:  A connection to the client, established with the master key
                The key uid of the key that should be deleted
    """

    print("Are you sure you want to delete this key: ", key_uid)
    delte = str(input("[y/n]: "))

    if delte in ["y", "Y", "Yes", "yes"]:
        client.delete_key(key_uid)


def main():
    """
    Main function in the key_file

    Uncomment the functions you want to use:
    for 'create' and 'get_keys' just the function call, for all others also uncomment
    the input of the key_uid


    """
    client = meilisearch.Client("http://localhost:7701", Api_key.MASTER_KEY)

    # create_key(client)
    get_keys(client)

    # key_uid = str(input("Please enter the key  UID: "))
    # delete_key(client, key_uid)
    # key = get_key(client, key_uid)
    # save_key(client, key_uid)


if __name__ == "__main__":
    main()
