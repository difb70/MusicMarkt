## 2FA client
The program `mobileApp.py` emulates the client mobile phone. This program is used by the client whenever he tries to login, because a authentication code is sent for the second  part of the login process

### Setup
1. Generate client key pair
    ```shell
    ./musicmarkt/client/client_keys/client_keys_generator.sh
    ```

2. Copy server public key and secret shared key to the client directory
    ```shell
    # if the public key or the secret shared key aren't yet generated : 
    /musicmarkt/keys/2fa_keys/api_keys_generator.sh
    /musicmarkt/keys/2fa_keys/generate_secret_key.sh
    python3 /musicmarkt/keys/2fa_keys/fernet_key.py
    python3 /musicmarkt/keys/2fa_keys/hash_secret.py

    # copy to the client key directory the shared keys
    cp /musicmarkt/keys/2fa_keys/secretKey.* /musicmarkt/client/client_keys/

    # copy to the client key directory the api public key
    cp /musicmarkt/keys/2fa_keys/apiPublic.pem  /musicmarkt/client/client_keys/
    ```

---
### Run

```shell
python3 /musicmarkt/client/mobileApp.py
```