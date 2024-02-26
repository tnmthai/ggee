def ee_init(
    token_name="EARTHENGINE_TOKEN",
    auth_mode="notebook",
    service_account=False,
    auth_args={},
    user_agent_prefix="ggee",
    **kwargs,
):
    """Authenticates Earth Engine and initializes an Earth Engine session."""
    import httplib2
    import ee
    import os
    import json
    # from .__init__ import __version__

    user_agent = f"{user_agent_prefix}"
    auth_args["auth_mode"] = auth_mode

    if ee.data._credentials is None:
        ee_token = os.environ.get(token_name)

        if service_account:
            try:
                credential_file_path = os.path.expanduser(
                    "~/.config/earthengine/private-key.json"
                )

                if os.path.exists(credential_file_path):
                    with open(credential_file_path) as f:
                        token_dict = json.load(f)
                    service_account = token_dict["client_email"]
                    private_key = token_dict["private_key"]
                    print(service_account, private_key)
                    credentials = ee.ServiceAccountCredentials(
                        service_account, key_data=private_key
                    )
                    ee.Initialize(credentials, **kwargs)

            except Exception as e:
                raise Exception(e)
 
        else:
            try:
                if ee_token is not None:
                    credential_file_path = os.path.expanduser(
                        "~/.config/earthengine/credentials"
                    )
                    if not os.path.exists(credential_file_path):
                        os.makedirs(
                            os.path.dirname(credential_file_path), exist_ok=True
                        )
                    with open(credential_file_path, "w") as f:
                        f.write(ee_token)
                ee.Initialize(**kwargs)

            except Exception:
                ee.Authenticate(**auth_args)
                ee.Initialize(**kwargs)

    ee.data.setUserAgent(user_agent)

def get_token():
    """Get Earth Engine token.

    Returns:
        dict: The Earth Engine token.
    """
    import os, json

    credential_file_path = os.path.expanduser("~/.config/earthengine/credentials")

    if os.path.exists(credential_file_path):
        with open(credential_file_path, "r") as f:
            credentials = json.load(f)
            return credentials
    else:
        print("Earth Engine credentials not found. Please run ggee.ee_init()")
        return None